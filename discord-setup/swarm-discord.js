/**
 * SWARM OS Discord Integration
 * Posts updates from agents to Discord channels via webhooks
 */

class SWARMDiscord {
    constructor() {
        // Webhook URLs - loaded from config
        this.webhooks = {
            general: 'https://discordapp.com/api/webhooks/1471913803968024841/MXfEOeJcTzxU5ltMHntGb_mQ0hBE2urFaGvrj7GfMvyltyjIKUHua9H2mTNWy0TC--9Z',
            fitness: 'https://discordapp.com/api/webhooks/1471913851065995294/c2glIe8MoUyQ-93FphYVbF5nvyleiHXZTbpCSC497FXdtcl-qadbQa6_B2mUemgzKDD_',
            sourcing: 'https://discordapp.com/api/webhooks/1471913899329589420/bikMi7tgGGrVdgbTZ15_QC06N4viqFR20oqXgK1jTCiUKS_8ds-Sg4CNaRBMz1JRVogs',
            audit: 'https://discordapp.com/api/webhooks/1471913903842656306/u6zO2zB8l7GhMbX-9RAntEIvywk528wA7ZuKABwmC3gSDVKTfVewArd_Cmhsphtr2Pi9',
            logs: 'https://discordapp.com/api/webhooks/1471913904937373761/oIY5wXNXkCrJ94vNKTWcK1tNuASp4t07u_rG_4Jmv6hVHvXrpv5o4-pGs13HWuihSl9Q'
        };
        
        this.agents = {
            stu: { name: 'Stu', color: 0x00D4AA, avatar: null },
            fitbot: { name: 'FitBot', color: 0x00CC41, avatar: null },
            sourcebot: { name: 'SourceBot', color: 0x00AAFF, avatar: null },
            auditbot: { name: 'AuditBot', color: 0xFF4444, avatar: null }
        };
    }
    
    /**
     * Send a message to a Discord channel
     */
    async send(channel, message, options = {}) {
        const webhook = this.webhooks[channel];
        if (!webhook) {
            console.error(`No webhook configured for channel: ${channel}`);
            return false;
        }
        
        const payload = {
            content: message,
            username: options.username || 'SWARM-System',
            avatar_url: options.avatar || null
        };
        
        if (options.embeds) {
            payload.embeds = options.embeds;
        }
        
        try {
            const response = await fetch(webhook, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            if (response.ok) {
                console.log(`✅ Message sent to #${channel}`);
                return true;
            } else {
                console.error(`❌ Failed to send to #${channel}:`, response.status);
                return false;
            }
        } catch (error) {
            console.error(`❌ Error sending to #${channel}:`, error);
            return false;
        }
    }
    
    /**
     * Send an embed message (rich formatting)
     */
    async sendEmbed(channel, embed, options = {}) {
        const webhook = this.webhooks[channel];
        if (!webhook) return false;
        
        const payload = {
            embeds: [embed],
            username: options.username || 'SWARM-System',
            avatar_url: options.avatar || null
        };
        
        try {
            const response = await fetch(webhook, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            return response.ok;
        } catch (error) {
            console.error('Discord webhook error:', error);
            return false;
        }
    }
    
    /**
     * Agent-specific message methods
     */
    async stu(message, options = {}) {
        return this.send('general', message, { username: 'Stu', ...options });
    }
    
    async fitbot(message, options = {}) {
        return this.send('fitness', message, { username: 'FitBot', ...options });
    }
    
    async sourcebot(message, options = {}) {
        return this.send('sourcing', message, { username: 'SourceBot', ...options });
    }
    
    async auditbot(message, options = {}) {
        return this.send('audit', message, { username: 'AuditBot', ...options });
    }
    
    async log(message, level = 'info') {
        const timestamp = new Date().toISOString();
        const prefix = level === 'error' ? '🔴' : level === 'warn' ? '🟡' : '🟢';
        return this.send('logs', `${prefix} [${timestamp}] ${message}`, { username: 'SWARM-System' });
    }
    
    /**
     * Mission updates
     */
    async missionStart(mission) {
        const embed = {
            title: `🔴 NEW MISSION: ${mission.name}`,
            description: mission.description,
            color: 0xFF4444,
            fields: [
                { name: 'Assigned', value: mission.agent, inline: true },
                { name: 'Priority', value: mission.priority, inline: true },
                { name: 'Status', value: '🔵 In Progress', inline: true }
            ],
            timestamp: new Date().toISOString()
        };
        
        await this.sendEmbed('missions', embed, { username: 'Stu' });
        await this.log(`Mission started: ${mission.name} (${mission.agent})`);
    }
    
    async missionComplete(mission) {
        const embed = {
            title: `✅ MISSION COMPLETE: ${mission.name}`,
            color: 0x00CC41,
            fields: [
                { name: 'Agent', value: mission.agent, inline: true },
                { name: 'Duration', value: mission.duration, inline: true }
            ],
            timestamp: new Date().toISOString()
        };
        
        await this.sendEmbed('missions', embed, { username: 'Stu' });
        await this.log(`Mission completed: ${mission.name}`);
    }
    
    /**
     * Fitness updates
     */
    async workoutLogged(workout) {
        const embed = {
            title: '💪 Workout Logged',
            description: workout.description,
            color: 0x00CC41,
            fields: [
                { name: 'Duration', value: workout.duration, inline: true },
                { name: 'Calories', value: workout.calories, inline: true }
            ],
            timestamp: new Date().toISOString()
        };
        
        await this.sendEmbed('fitness', embed, { username: 'FitBot' });
    }
    
    async weightUpdate(weight, goal) {
        const progress = ((goal / weight) * 100).toFixed(1);
        const embed = {
            title: '📊 Weight Update',
            description: `Current: **${weight} lbs** | Goal: **${goal} lbs**`,
            color: 0x00CC41,
            fields: [
                { name: 'Progress', value: `${progress}% to goal`, inline: true },
                { name: 'Remaining', value: `${(weight - goal).toFixed(1)} lbs`, inline: true }
            ],
            timestamp: new Date().toISOString()
        };
        
        await this.sendEmbed('fitness', embed, { username: 'FitBot' });
    }
    
    /**
     * System status
     */
    async systemOnline() {
        const embed = {
            title: '🚀 SWARM OS ONLINE',
            description: 'All systems operational. Ready for commands.',
            color: 0x00D4AA,
            fields: [
                { name: 'Agents', value: '4 Active', inline: true },
                { name: 'Channels', value: '5 Connected', inline: true },
                { name: 'Status', value: '🟢 Operational', inline: true }
            ],
            timestamp: new Date().toISOString()
        };
        
        await this.sendEmbed('general', embed, { username: 'Stu' });
        await this.log('SWARM OS initialized');
    }
    
    /**
     * Test all webhooks
     */
    async testAll() {
        const results = {};
        
        for (const [channel, url] of Object.entries(this.webhooks)) {
            const success = await this.send(channel, `🧪 Test message from SWARM OS Dashboard`, {
                username: 'SWARM-Test'
            });
            results[channel] = success ? '✅' : '❌';
        }
        
        console.log('Webhook test results:', results);
        return results;
    }
}

// Export for use in dashboard
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SWARMDiscord;
}
