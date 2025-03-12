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
    <td class="score ctf-score" @click="showLightSubmits">
      <div class="score-container">
        <div class="score-value">{{ teamData.ctfScore }}</div>
        <div v-if="teamData.maxSubmit > 0" class="submit-bubble" :class="{ 'bubble-animate': isAnimating }">
          {{ isAnimating ? currentBubbleContent : remainingSubmits }}
        </div>
      </div>
    </td>
    <td class="score koh-score" @click="toggleKohScore">
      <div class="score-value" :class="{ 'hidden-score': !showKohScore }">
        {{ showKohScore ? teamData.kohScore : '?' }}
      </div>
    </td>
    <td class="score total-score">
      <div class="score-container">
        <div class="cyber-box">{{ currentTotalScore }}</div>
      </div>
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
      isHovered: false,
      isAnimating: false,
      currentBubbleContent: '',
      currentSubmitIndex: 0,
      animationQueue: [],
      hasPlayedAnimation: false,  // 新增标志位
      initialCtfScore: 0,
      hasInitialized: false
    }
  },
  computed: {
    progressPercentage() {
      return (this.teamData.solved / this.teamData.total) * 100
    },
    currentTotalScore() {
      return this.teamData.ctfScore + (this.showKohScore ? this.teamData.kohScore : 0)
    },
    remainingSubmits() {
      return this.teamData.maxSubmit - this.currentSubmitIndex;
    }
  },
  methods: {
    toggleKohScore() {
      this.$emit('koh-score-toggle', {
        teamId: this.teamData.name,
        showKoh: !this.showKohScore
      });
    },
    async showLightSubmits() {
      if (this.isAnimating || !this.teamData.lightSubmit || 
          this.teamData.maxSubmit === 0 || 
          this.currentSubmitIndex >= this.teamData.maxSubmit) return;
      
      if (!this.hasInitialized) {
        this.initialCtfScore = this.teamData.ctfScore;
        this.hasInitialized = true;
      }

      this.isAnimating = true;
      this.currentSubmitIndex++;
      
      const submission = this.teamData.lightSubmit.find(s => s[0] === this.currentSubmitIndex);
      
      if (submission) {
        this.currentBubbleContent = `+${submission[1]}`;
        // 等待动画完成
        await new Promise(resolve => setTimeout(resolve, 2000));
        // 更新分数和进度
        this.teamData.ctfScore = this.initialCtfScore + 
          this.teamData.lightSubmit
            .filter(s => s[0] <= this.currentSubmitIndex)
            .reduce((sum, s) => sum + s[1], 0);
        this.teamData.solved += 1;
      } else {
        this.currentBubbleContent = 'Failed';
        await new Promise(resolve => setTimeout(resolve, 2000));
      }

      this.isAnimating = false;
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

.score-container {
  position: relative;
  display: inline-block;
}

.submit-bubble {
  position: absolute;
  top: -10px;
  right: -15px;
  background: #ff0080;
  color: #fff;
  border-radius: 50%;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8em;
  font-weight: bold;
  animation: bubble-pop 0.2s ease-out, bubble-float 2s ease-in-out infinite;
  box-shadow: 0 0 10px #ff0080;
  z-index: 2;
  transition: content 0.3s ease;
}

.bubble-animate {
  animation: bubble-rise 1s ease-out forwards;
}

@keyframes bubble-pop {
  0% {
    transform: scale(0);
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes bubble-float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

@keyframes bubble-rise {
  0% {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
  50% {
    transform: scale(1.5) translateY(-20px);
    opacity: 0.8;
  }
  100% {
    transform: scale(2) translateY(-40px);
    opacity: 0;
  }
}
</style>