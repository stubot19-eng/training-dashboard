// Twitter/X API Proxy Server
// Secure backend endpoint - token never exposed to frontend

require('dotenv').config();
const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());

const X_BEARER_TOKEN = process.env.X_BEARER_TOKEN;
const PORT = process.env.PORT || 3002;

// Twitter user IDs
const TWITTER_USERS = {
    wojespn: '50323173',
    ShamsCharania: '178580925',
    KnicksNation: '136205834',
    NetsDaily: '18584815',
    Yankees: '40927173',
    Mets: '39367703'
};

// Proxy endpoint for tweets
app.get('/api/tweets/:username', async (req, res) => {
    try {
        const username = req.params.username;
        const userId = TWITTER_USERS[username];
        
        if (!userId) {
            return res.status(404).json({ error: 'User not found' });
        }
        
        const response = await fetch(`https://api.x.com/2/users/${userId}/tweets?max_results=5&tweet.fields=created_at,public_metrics`, {
            headers: {
                'Authorization': `Bearer ${X_BEARER_TOKEN}`
            }
        });
        
        if (!response.ok) {
            throw new Error(`X API error: ${response.status}`);
        }
        
        const data = await response.json();
        res.json(data);
        
    } catch (error) {
        console.error('Twitter proxy error:', error);
        res.status(500).json({ error: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`🐦 Twitter proxy server running on port ${PORT}`);
});
