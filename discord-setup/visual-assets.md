# SWARM OS Visual Assets Guide

## 🎨 Brand Specifications

### Color Palette

| Name | Hex | Usage |
|------|-----|-------|
| SWARM Gold | `#FFD700` | @CEO role, highlights, premium |
| Orchestrator Teal | `#00D4AA` | @LeadOrchestrator, Stu branding |
| Agent Blurple | `#7289DA` | @Agent role, bot integrations |
| SWARM Dark | `#0A0A0F` | Backgrounds, dark mode base |
| SWARM Grey | `#2A2A35` | Panels, secondary surfaces |
| Alert Green | `#00C851` | Success, online status |
| Alert Yellow | `#FFBB33` | Warning, advisory |
| Alert Red | `#FF4444` | Critical, blocked |

### Typography

- **Headers:** All caps, bold, spaced with ━━━━ lines
- **Agent names:** Title case, emoji prefix
- **System text:** Monospace for logs, regular for chat

---

## 🖼️ Server Icon

### Specifications
- **Size:** 512x512px (Discord will scale)
- **Format:** PNG with transparency
- **Style:** Futuristic, tech-focused

### Design Concept

```
┌─────────────────┐
│   ◉────◉       │
│    \   /       │  ← Hexagonal swarm node
│     \ /        │
│   ──●──        │  ← Central core (glowing)
│     / \        │
│    /   \       │
│   ◉────◉       │
│                 │
│   S W A R M     │
│    O S          │
└─────────────────┘
```

**Elements:**
- Dark background (#0A0A0F)
- Glowing teal center (#00D4AA)
- 3 orbiting nodes in gold (#FFD700)
- Hexagonal grid pattern subtle

---

## 🤖 Agent Avatars

### Stu (LeadOrchestrator)
- **Style:** Professional, authoritative
- **Base:** Geometric hexagon with orbiting elements
- **Color:** Teal (#00D4AA) with white accents
- **Icon:** Central node with 3 satellites

### FitBot
- **Style:** Energetic, athletic
- **Base:** Geometric design with pulse/activity lines
- **Color:** Green gradient (#00C851 to #00D4AA)
- **Icon:** Heart rate pulse + hexagon

### SourceBot
- **Style:** Industrial, precise
- **Base:** Crate/box with circuit patterns
- **Color:** Orange (#FF8800) with steel grey
- **Icon:** Package with network connections

### AuditBot
- **Style:** Alert, watchful
- **Base:** Shield or eye motif
- **Color:** Red (#FF4444) with dark grey
- **Icon:** Scanning reticle or shield with checkmark

---

## 📊 Embed Styling

### Standard Agent Update Embed

```json
{
  "embeds": [{
    "title": "🤖 Agent Name | Task Update",
    "description": "Brief description of update",
    "color": 0x00D4AA,
    "fields": [
      {
        "name": "Status",
        "value": "🟢 Complete / 🔵 In Progress / 🔴 Blocked",
        "inline": true
      },
      {
        "name": "Timestamp",
        "value": "2026-02-13 16:43 UTC",
        "inline": true
      }
    ],
    "footer": {
      "text": "SWARM OS v1.0 | Agent ID"
    }
  }]
}
```

### Color Mapping

| Agent | Embed Color (Decimal) | Hex |
|-------|----------------------|-----|
| Stu | 5461 | #00D4AA |
| FitBot | 52225 | #00CC41 |
| SourceBot | 43775 | #00AAFF |
| AuditBot | 16733525 | #FF4444 |
| System | 9868950 | #96A9C6 |

---

## 🎯 Message Formatting Templates

### Mission Announcement

```
🔴 **NEW MISSION DEPLOYED**
━━━━━━━━━━━━━━━━━━━━━━━━━━

**Mission ID:** M-2026-02-13-001
**Designation:** [Name]
**Priority:** High | Medium | Low
**Assigned Agent:** @[AgentName]

**Objective:**
[Clear description of what needs to be done]

**Success Criteria:**
• [Criterion 1]
• [Criterion 2]
• [Criterion 3]

**ETA:** [Time estimate]

Status: 🟡 Planning → 🔵 In Progress
```

### Status Update

```
📝 **STATUS UPDATE | [Agent Name]**

Previous: [Old status]
Current:  [New status]

Details:
[What changed and why]

Next Action: [What's coming next]
ETA: [When to expect it]
```

### System Alert

```
⚠️ **SYSTEM ALERT | [Severity]**
━━━━━━━━━━━━━━━━━━━━━━━━━━

**Alert ID:** A-001
**Source:** [Agent/Component]
**Detected:** [Timestamp]

**Issue:**
[Description of the problem]

**Impact:**
[What this affects]

**Action Required:**
[What needs to happen to resolve]

AuditBot is monitoring.
```

---

## 🔗 Placeholder Avatar URLs

For testing before custom avatars are ready:

- **Stu:** https://cdn.discordapp.com/embed/avatars/0.png
- **FitBot:** https://cdn.discordapp.com/embed/avatars/1.png
- **SourceBot:** https://cdn.discordapp.com/embed/avatars/2.png
- **AuditBot:** https://cdn.discordapp.com/embed/avatars/3.png

Replace with custom URLs once created.

---

## 📱 Mobile Considerations

- Keep embeds under 6000 characters total
- Use inline fields for related data
- Critical info goes in description (always visible)
- Test formatting on mobile Discord app

---

## ✅ Asset Checklist

- [ ] Server icon (512x512 PNG)
- [ ] Stu avatar (256x256 PNG)
- [ ] FitBot avatar (256x256 PNG)
- [ ] SourceBot avatar (256x256 PNG)
- [ ] AuditBot avatar (256x256 PNG)
- [ ] Category icons (if using Discord bots for fancy formatting)
- [ ] Embed templates tested
- [ ] Mobile formatting verified
