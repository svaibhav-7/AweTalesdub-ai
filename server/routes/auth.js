const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const { query } = require('../db');
const router = express.Router();

// Generate JWT token
const generateToken = (user) => {
    return jwt.sign(
        { id: user.id, email: user.email, role: user.role },
        process.env.JWT_SECRET,
        { expiresIn: process.env.JWT_EXPIRES_IN }
    );
};

// @route   POST /api/auth/register
// @desc    Register a new user
router.post('/register', async (req, res) => {
    const { name, email, password } = req.body;
    try {
        const userExists = await query('SELECT * FROM users WHERE email = $1', [email]);
        if (userExists.rows.length > 0) {
            return res.status(400).json({ error: 'Email already registered.' });
        }

        const salt = await bcrypt.genSalt(10);
        const hashedPassword = await bcrypt.hash(password, salt);

        // Initial 10 credits for freemium model
        const newUser = await query(
            'INSERT INTO users (name, email, password, role, credits, plan) VALUES ($1, $2, $3, $4, $5, $6) RETURNING id, name, email, role, credits, plan',
            [name, email, hashedPassword, email === process.env.SUPER_ADMIN_EMAIL ? 'admin' : 'user', 10, 'free']
        );

        const token = generateToken(newUser.rows[0]);
        res.cookie('token', token, { httpOnly: true, maxAge: 7 * 24 * 60 * 60 * 1000 });
        res.status(201).json({ message: 'Registration successful', user: newUser.rows[0] });

    } catch (err) {
        console.error(err.message);
        res.status(500).json({ error: 'Server error during registration.' });
    }
});

// @route   POST /api/auth/login
// @desc    Authenticate user & get token
router.post('/login', async (req, res) => {
    const { email, password } = req.body;
    try {
        const userRaw = await query('SELECT * FROM users WHERE email = $1', [email]);
        if (userRaw.rows.length === 0) {
            return res.status(400).json({ error: 'Invalid credentials.' });
        }

        const user = userRaw.rows[0];
        const isMatch = await bcrypt.compare(password, user.password);

        if (!isMatch) {
            return res.status(400).json({ error: 'Invalid credentials.' });
        }

        const token = generateToken(user);
        // Set HTTP Only Cookie
        res.cookie('token', token, { httpOnly: true, maxAge: 7 * 24 * 60 * 60 * 1000 });

        // Scrub password
        delete user.password;
        res.json({ message: 'Logged in effectively', user });

    } catch (err) {
        console.error(err.message);
        res.status(500).json({ error: 'Server error during login.' });
    }
});

// @route   POST /api/auth/logout
router.post('/logout', (req, res) => {
    res.clearCookie('token');
    res.json({ message: 'Logged out.' });
});

module.exports = router;
