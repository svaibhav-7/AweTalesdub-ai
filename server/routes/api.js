const express = require('express');
const { query } = require('../db');
const { requireAuth } = require('../middleware/authMiddleware');
const router = express.Router();

// @route   GET /api/user/me
// @desc    Get current logged in user details
router.get('/user/me', requireAuth, async (req, res) => {
    try {
        const userRaw = await query('SELECT id, name, email, role, credits, plan, created_at FROM users WHERE id = $1', [req.user.id]);
        if (userRaw.rows.length === 0) return res.status(404).json({ error: 'User not found' });

        // Check if God-Mode bypasses credit view
        const isGodMode = userRaw.rows[0].email === process.env.SUPER_ADMIN_EMAIL;
        if (isGodMode) userRaw.rows[0].credits = '∞';

        res.json({ user: userRaw.rows[0] });
    } catch (err) {
        res.status(500).json({ error: 'Server error' });
    }
});

// @route   GET /api/jobs
// @desc    Get dubbing jobs for current user
router.get('/jobs', requireAuth, async (req, res) => {
    try {
        const jobs = await query('SELECT * FROM dub_jobs WHERE user_id = $1 ORDER BY created_at DESC', [req.user.id]);
        res.json({ jobs: jobs.rows });
    } catch (err) {
        res.status(500).json({ error: 'Server error' });
    }
});

// @route   POST /api/jobs/create
// @desc    Initiate a new dubbing job (deducts credit)
router.post('/jobs/create', requireAuth, async (req, res) => {
    const { source_url, target_language } = req.body;
    try {
        // 1. Verify credits
        const userRaw = await query('SELECT credits, email FROM users WHERE id = $1', [req.user.id]);
        const isGodMode = userRaw.rows[0].email === process.env.SUPER_ADMIN_EMAIL;

        if (!isGodMode && userRaw.rows[0].credits < 1) {
            return res.status(402).json({ error: 'Insufficient credits. Please upgrade your plan.' });
        }

        // 2. Deduct credit (skip if God-Mode)
        if (!isGodMode) {
            await query('UPDATE users SET credits = credits - 1 WHERE id = $1', [req.user.id]);
        }

        // 3. Create Job
        const newJob = await query(
            'INSERT INTO dub_jobs (user_id, source_url, target_language, cost_credits) VALUES ($1, $2, $3, $4) RETURNING *',
            [req.user.id, source_url, target_language, 1]
        );

        // *In Reality, this is where we would trigger the FastAPI Background Python Worker*

        res.json({ message: 'Dubbing job initialized', job: newJob.rows[0] });
    } catch (err) {
        res.status(500).json({ error: 'Server error' });
    }
});

// @route   GET /api/announcements
// @desc    Get active global announcements
router.get('/announcements', async (req, res) => {
    try {
        const announcements = await query('SELECT * FROM global_announcements WHERE active = true ORDER BY created_at DESC LIMIT 5');
        res.json({ announcements: announcements.rows });
    } catch (err) {
        res.status(500).json({ error: 'Server error' });
    }
});

module.exports = router;
