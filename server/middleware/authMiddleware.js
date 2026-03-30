const jwt = require('jsonwebtoken');

// Verifies User JWT
const requireAuth = (req, res, next) => {
    const token = req.cookies?.token;
    if (!token) return res.status(401).json({ error: 'Unauthorized Access. Please login.' });

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        req.user = decoded; // { id, email, role }
        next();
    } catch (err) {
        res.status(401).json({ error: 'Invalid or Expired Token.' });
    }
};

// Strict check for God-Mode Sasi Vaibhav Admin
const requireSuperAdmin = (req, res, next) => {
    const token = req.cookies?.token;
    if (!token) return res.status(401).json({ error: 'Unauthorized Access. Please login.' });

    try {
        const decoded = jwt.verify(token, process.env.JWT_SECRET);
        // Hardcoded check referencing the environment file constraint
        if (decoded.email !== process.env.SUPER_ADMIN_EMAIL) {
            return res.status(403).json({ error: 'Forbidden. You do not have God-Mode privileges.' });
        }
        req.user = decoded;
        next();
    } catch (err) {
        res.status(401).json({ error: 'Invalid or Expired Token.' });
    }
};

module.exports = { requireAuth, requireSuperAdmin };
