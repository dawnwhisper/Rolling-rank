<template>
    <div class="scoreboard-container">
        <div class="cyber-header">
            <h1 class="cyber-title">Scoreboard</h1>
        </div>
        
        <div class="table-wrapper">
            <table class="cyber-table">
                <thead>
                    <tr>
                        <th class="rank-column">#</th>
                        <th class="team-column">战队名称</th>
                        <th class="challenge-column">答题进度</th>
                        <th class="score-column">CTF得分</th>
                        <th class="score-column">KOH得分</th>
                        <th class="total-column">总分</th>
                    </tr>
                </thead>
                <tbody>
                    <TeamScoreRow 
                        v-for="(team, index) in sortedTeams" 
                        :key="team.name"
                        :team-data="team"
                        :rank="team.nonCompeting ? '*' : calculateRank(team)"
                        :show-koh-score="visibleKohScores.has(team.name)"
                        @koh-score-toggle="handleKohScoreToggle"
                    />
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import TeamScoreRow from '../components/TeamScoreRow.vue'
import teamsData from '../assets/data.json'

export default {
    name: 'Scoreboard',
    components: {
        TeamScoreRow
    },
    data() {
        return {
            teams: teamsData,
            sortKey: 'totalScore',
            sortAsc: false,
            visibleKohScores: new Set()
        }
    },
    computed: {
        sortedTeams() {
            return [...this.teams].sort((a, b) => {
                const ctfhighest = 2982;
                const kohhighest = 900;                
                const aTotal = a.ctfScore / ctfhighest * 1000 * 0.7 + (this.visibleKohScores.has(a.name) ? a.kohScore : 0) / kohhighest * 100 * 0.3;
                const bTotal = b.ctfScore / ctfhighest * 1000 * 0.7 + (this.visibleKohScores.has(b.name) ? b.kohScore : 0) / kohhighest * 100 * 0.3;
                return bTotal - aTotal;
            });
        }
    },
    methods: {
        async fetchData() {
            try {
                // 实际使用时替换为真实的API调用
                // const response = await fetch('/api/scoreboard')
                // this.teams = await response.json()
            } catch (error) {
                console.error('Failed to fetch scoreboard data:', error)
            }
        },
        handleKohScoreToggle(event) {
            const newVisibleKohScores = new Set(this.visibleKohScores);
            if (event.showKoh) {
                newVisibleKohScores.add(event.teamId);
            } else {
                newVisibleKohScores.delete(event.teamId);
            }
            this.visibleKohScores = newVisibleKohScores;
        },
        calculateRank(team) {
            if (team.nonCompeting) return '*';
            const position = this.sortedTeams
                .filter(t => !t.nonCompeting)
                .findIndex(t => t.name === team.name);
            return position + 1;
        }
    },
    mounted() {
        this.fetchData()
        this.startRefreshTimer()
    }
}
</script>

<style scoped>
.scoreboard-container {
    width: 80%;
    max-width: 1200px;
    margin: 50px auto;
    padding: 30px;
    background: rgba(0, 0, 0, 0.8);
    border: 1px solid #0ff;
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    position: relative;
}

.table-wrapper {
    max-height: calc(80vh - 150px);
    overflow-y: auto;
    margin-right: -15px;
    padding-right: 15px;
}

.table-wrapper::-webkit-scrollbar {
    width: 0;
    height: 0;
}

.table-wrapper::-webkit-scrollbar-track {
    background: transparent;
}

.table-wrapper::-webkit-scrollbar-thumb {
    background: transparent;
}

.cyber-header {
    margin-bottom: 30px;
    padding: 20px;
    border-bottom: 2px solid rgba(0, 255, 255, 0.3);
    text-align: center;
    position: relative;
}

.cyber-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.5em;
    color: #0ff;
    text-shadow: 0 0 10px #0ff;
    margin: 0;
    letter-spacing: 4px;
    position: relative;
    display: inline-block;
}

.cyber-title::before,
.cyber-title::after {
    content: 'Scoreboard';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

.cyber-title::before {
    color: #ff0080;
    z-index: -2;
    animation: glitch 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) both infinite;
}

.cyber-title::after {
    color: #0ff;
    z-index: -1;
    animation: glitch 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) reverse both infinite;
}

.refresh-timer {
    font-family: 'Courier New', monospace;
    color: #0ff;
    padding: 5px 10px;
    border: 1px solid #0ff;
    background: rgba(0, 255, 255, 0.1);
}

.cyber-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    background: rgba(0, 20, 30, 0.95);
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.1);
    table-layout: fixed;
    overflow: auto;
    max-height: calc(80vh - 100px);
}

.cyber-table::-webkit-scrollbar {
    width: 0;
    height: 0;
}

.cyber-table::-webkit-scrollbar-track {
    background: transparent;
}

.cyber-table::-webkit-scrollbar-thumb {
    background: transparent;
}

.cyber-table thead {
    position: sticky;
    top: 0;
    z-index: 1;
    background: rgba(0, 20, 30, 0.95);
}

th, td {
    padding: 15px;
    text-align: left;
    box-sizing: border-box;
}

.rank-column {
    width: 8%;
    text-align: center;
}

.team-column {
    width: 25%;
    padding-left: 20px;
}

.challenge-column {
    width: 22%;
    text-align: center;
}

.score-column {
    width: 15%;
    text-align: center;
}

.total-column {
    width: 15%;
    text-align: center;
}

tbody td {
    padding: 15px;
    vertical-align: middle;
    overflow-y: auto;
}

thead th {
    font-family: 'Orbitron', sans-serif;
    background: rgba(0, 255, 255, 0.1);
    border-bottom: 2px solid #0ff;
    position: sticky;
    top: 0;
    z-index: 1;
}

@keyframes glow {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.cyber-table thead th {
    padding: 15px;
    text-align: center;
    background: rgba(0, 40, 50, 0.9);
    color: #0ff;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.1em;
    text-shadow: 0 0 5px #0ff;
    border-bottom: 2px solid #0ff;
    transition: all 0.3s ease;
    cursor: pointer;
}

.cyber-table thead th:hover {
    background: rgba(0, 255, 255, 0.2);
    text-shadow: 0 0 8px #0ff;
}
</style>