<template>
  <tr class="team-score-row" :class="{ 'row-hover': isHovered }" @mouseover="isHovered = true" @mouseleave="isHovered = false">
    <td class="rank">{{ rank }}</td>
    <td class="team-name">{{ teamData.name }}</td>
    <td class="challenge-status">
      <div class="progress-container">
        <div class="progress-bar" :style="{ width: progressPercentage + '%' }">
          {{ teamData.solved }}/{{ teamData.total }}
        </div>
      </div>
    </td>
    <td class="score ctf-score">
      <div class="score-value">{{ teamData.ctfScore }}</div>
    </td>
    <td class="score koh-score" @click="toggleKohScore">
      <div class="score-value" :class="{ 'hidden-score': !showKohScore }">
        {{ showKohScore ? teamData.kohScore : '?' }}
      </div>
    </td>
    <td class="score total-score">
      <div class="cyber-box">{{ currentTotalScore }}</div>
    </td>
  </tr>
</template>

<script>
export default {
  name: 'TeamScoreRow',
  props: {
    teamData: {
      type: Object,
      required: true
    },
    rank: {
      type: Number,
      required: true
    },
    showKohScore: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      isHovered: false
    }
  },
  computed: {
    progressPercentage() {
      return (this.teamData.solved / this.teamData.total) * 100
    },
    currentTotalScore() {
      return this.teamData.ctfScore + (this.showKohScore ? this.teamData.kohScore : 0)
    }
  },
  methods: {
    toggleKohScore() {
      this.$emit('koh-score-toggle', {
        teamId: this.teamData.name,
        showKoh: !this.showKohScore
      });
    }
  }
}
</script>

<style scoped>
.team-score-row {
  background: rgba(0, 0, 0, 0.8);
  color: #0ff;
  transition: all 0.3s ease;
  border-bottom: 1px solid #0ff3;
}

.row-hover {
  background: rgba(0, 255, 255, 0.1);
  text-shadow: 0 0 5px #0ff;
}

.team-name {
  padding: 10px;
  color: #0ff;
  font-family: 'Orbitron', sans-serif;
  text-align: left;
  padding-left: 20px;
}

.progress-container {
  width: 100%;
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid #0ff3;
  height: 20px;
}

.progress-bar {
  background: linear-gradient(90deg, #0ff, #00ff9d);
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #000;
  font-weight: bold;
  text-shadow: none;
  transition: width 0.5s ease;
}

.score {
  text-align: center;
  font-size: 1.2em;
  font-family: 'Orbitron', sans-serif;
}

.score-value {
  background: rgba(0, 255, 255, 0.1);
  padding: 5px;
  border: 1px solid #0ff3;
  display: inline-block;
  min-width: 80px;
}

.cyber-box {
  background: linear-gradient(45deg, #000, #002);
  border: 1px solid #0ff;
  padding: 5px 15px;
  position: relative;
  box-shadow: 0 0 10px #0ff5;
  display: inline-block;
}

.cyber-box::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  border: 2px solid #0ff;
  clip-path: polygon(0 10px, 10px 0, calc(100% - 10px) 0, 100% 10px, 100% calc(100% - 10px), calc(100% - 10px) 100%, 10px 100%, 0 calc(100% - 10px));
}

.team-score-row td {
  padding: 15px;
  text-align: center;
}

.team-name {
  text-align: left;
  padding-left: 20px;
}

.challenge-status {
  text-align: center;
}

.score {
  text-align: center;
}

.rank {
  width: 8%;
  text-align: center;
  font-family: 'Orbitron', sans-serif;
  color: #0ff;
  font-weight: bold;
}

.hidden-score {
  cursor: pointer;
  background: rgba(0, 255, 255, 0.05);
}

.hidden-score:hover {
  background: rgba(0, 255, 255, 0.2);
}
</style>