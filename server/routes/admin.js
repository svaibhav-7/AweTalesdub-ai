const express = require('express');
const { query } = require('../db');
const { requireSuperAdmin } = require('../middleware/authMiddleware');
const router = express.Router();

// ALL ROUTES HERE ARE GUARDED BY requireSuperAdmin
// Only Sasi Vaibhav (as defined in .env) can access these

// @route   GET /api/admin/stats
// @desc    Get absolute platform totals
router.get('/stats', requireSuperAdmin, async (req, res) => {
    try {
        const totalUsers = await query('SELECT COUNT(*) FROM users');
        const totalJobs = await query('SELECT COUNT(*) FROM dub_jobs');
        const recentActivity = await query('SELECT users.name, dub_jobs.target_language, dub_jobs.created_at FROM dub_jobs JOIN users ON dub_jobs.user_id = users.id ORDER BY dub_jobs.created_at DESC LIMIT 10');

        res.json({
            metrics: {
                users: parseInt(totalUsers.rows[0].count),
                jobs_processed: parseInt(totalJobs.rows[0].count),
                revenue_estimate: parseInt(totalUsers.rows[0].count) * 9.99 // Rough MRR metric
            },
            activity: recentActivity.rows
        });
    } catch (err) {
        res.status(500).json({ error: 'Admin Stats Error' });
    }
});

// @route   GET /api/admin/users
// @desc    List all users with pagination
router.get('/users', requireSuperAdmin, async (req, res) => {
    const limit = parseInt(req.query.limit) || 50;
    const offset = parseInt(req.query.offset) || 0;
    try {
        const users = await query('SELECT id, name, email, plan, credits, created_at FROM users ORDER BY created_at DESC LIMIT $1 OFFSET $2', [limit, offset]);
        res.json({ users: users.rows });
    } catch (err) {
        res.status(500).json({ error: 'Admin Users Error' });
    }
});

// @route   POST /api/admin/override-credits
// @desc    Force set a user's credit balance
router.post('/override-credits', requireSuperAdmin, async (req, res) => {
    const { userId, newBalance } = req.body;
    try {
        await query('UPDATE users SET credits = $1 WHERE id = $2', [newBalance, userId]);
        res.json({ message: `Successfully updated user ${userId} to ${newBalance} credits.` });
    } catch (err) {
        res.status(500).json({ error: 'Admin Override Error' });
    }
});

// @route   POST /api/admin/broadcast
// @desc    Publish a global platform announcement
router.post('/broadcast', requireSuperAdmin, async (req, res) => {
    const { title, message } = req.body;
    try {
        const announcement = await query('INSERT INTO global_announcements (title, message) VALUES ($1, $2) RETURNING *', [title, message]);
        res.json({ message: 'Broadcast Live', announcement: announcement.rows[0] });
    } catch (err) {
        res.status(500).json({ error: 'Admin Broadcast Error' });
    }
});

module.exports = router;
