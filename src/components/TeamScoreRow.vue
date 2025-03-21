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
        <div v-for="bubble in activeBubbles" 
             :key="bubble.id"
             class="submit-bubble" 
             :class="{ 'bubble-animate': bubble.isAnimating }"
             :style="{ 
               '--random-x1': bubble.x1 + 'px',
               '--random-x2': bubble.x2 + 'px',
               '--random-x3': bubble.x3 + 'px',
               '--random-rotate': bubble.rotate + 'deg',
               '--random-scale': bubble.scale
             }">
          {{ bubble.content }}
        </div>
        <div v-if="teamData.maxSubmit > currentSubmitIndex && !isPlayingAnimation" 
             class="submit-bubble">
          {{ remainingSubmits }}
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
      hasInitialized: false,
      isResetting: false,
      randomX1: 0,
      randomX2: 0,
      randomX3: 0,
      randomRotate: 0,
      randomScale: 1,
      bubbleId: 0,
      activeBubbles: [],
      isPlayingAnimation: false
    }
  },
  computed: {
    progressPercentage() {
      return (this.teamData.solved / this.teamData.total) * 100
    },
    currentTotalScore() {
      const ctfhighest = 2300;
      const kohhighest = 900;
      return parseFloat(
        (
          this.teamData.ctfScore / ctfhighest * 1000 * 0.7 + (this.showKohScore ? this.teamData.kohScore : 0) / kohhighest * 100 * 0.4
        ).toFixed(3)
      )
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
    getRandomOffset() {
      return Math.random() * 60 - 30; // 生成-30到30之间的随机数
    },
    getRandomRotate() {
      return Math.random() * 360;
    },
    getRandomScale() {
      return 1.5 + Math.random() * 1;
    },
    async resetBubble() {
      this.isResetting = true;
      this.randomX1 = this.getRandomOffset();
      this.randomX2 = this.getRandomOffset();
      this.randomX3 = this.getRandomOffset();
      this.randomRotate = this.getRandomRotate();
      this.randomScale = this.getRandomScale();
      await new Promise(resolve => setTimeout(resolve, 100));
      this.isResetting = false;
    },
    createBubble(content, delay = 0) {
      setTimeout(() => {
        const bubble = {
          id: this.bubbleId++,
          content,
          isAnimating: true,
          x1: this.getRandomOffset(),
          x2: this.getRandomOffset(),
          x3: this.getRandomOffset(),
          rotate: this.getRandomRotate(),
          scale: this.getRandomScale()
        };
        this.activeBubbles.push(bubble);
        // 修改气泡存在时间为1秒
        setTimeout(() => {
          this.activeBubbles = this.activeBubbles.filter(b => b.id !== bubble.id);
        }, 1000);
        return bubble;
      }, delay);
    },

    async showLightSubmits() {
      if (!this.teamData.lightSubmit || 
          this.currentSubmitIndex >= this.teamData.maxSubmit) return;
      
      this.isPlayingAnimation = true;
      
      if (!this.hasInitialized) {
        this.initialCtfScore = this.teamData.ctfScore;
        this.hasInitialized = true;
      }

      let firstAnimation = true;
      let lastErrorDelay = 0;
      let wrong = 0;

      // 找到下一个正确提交
      const nextCorrectSubmission = this.teamData.lightSubmit.find(s => s[0] > this.currentSubmitIndex);
      
      // 如果没有下一个正确提交，播放剩余的错误提交
      if (!nextCorrectSubmission) {
        while (this.currentSubmitIndex < this.teamData.maxSubmit) {
          this.currentSubmitIndex++;
          const delay = firstAnimation ? 0 : (this.currentSubmitIndex - 1) * 500;
          this.createBubble('Failed', delay);
          lastErrorDelay = delay;
          firstAnimation = false;
        }
        // 等待所有错误动画完成
        await new Promise(resolve => setTimeout(resolve, lastErrorDelay + 1000));
        this.isPlayingAnimation = false;
        return;
      }
      
      // 播放到下一个正确提交之前的错误提交
      while (this.currentSubmitIndex < nextCorrectSubmission[0] - 1) {
        wrong = 1;
        this.currentSubmitIndex++;
        const delay = firstAnimation ? 0 : (this.currentSubmitIndex - 1) * 500;
        this.createBubble('Failed', delay);
        lastErrorDelay = delay;
        firstAnimation = false;
      }
      
      // 播放正确提交
      const delayBeforeCorrect = wrong === 0 ? 0 : lastErrorDelay + 500;
      this.currentSubmitIndex = nextCorrectSubmission[0];
      this.createBubble(`+${nextCorrectSubmission[1]}`, delayBeforeCorrect);
      
      // 等待所有动画完成后更新分数
      await new Promise(resolve => setTimeout(resolve, delayBeforeCorrect + 1000));
      
      this.teamData.ctfScore = this.initialCtfScore + 
        this.teamData.lightSubmit
          .filter(s => s[0] <= this.currentSubmitIndex)
          .reduce((sum, s) => sum + s[1], 0);
      this.teamData.solved += 1;
      
      this.isPlayingAnimation = false;
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
  box-shadow: 0 0 10px #ff0080;
  z-index: 2;
}

.bubble-animate {
  animation: bubble-rise 1s cubic-bezier(0.4, 0, 0.6, 1) forwards;
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
    transform: scale(1) translate(0, 0) rotate(0deg);
    opacity: 1;
  }
  25% {
    transform: scale(calc(var(--random-scale) * 0.5)) 
               translate(var(--random-x1), -100px)
               rotate(calc(var(--random-rotate) * 0.25deg));
    opacity: 0.9;
  }
  50% {
    transform: scale(calc(var(--random-scale) * 0.8)) 
               translate(var(--random-x2), -200px)
               rotate(calc(var(--random-rotate) * 0.5deg));
    opacity: 0.8;
  }
  75% {
    transform: scale(calc(var(--random-scale) * 0.9))
               translate(var(--random-x3), -300px)
               rotate(calc(var(--random-rotate) * 0.75deg));
    opacity: 0.7;
  }
  100% {
    transform: scale(var(--random-scale)) 
               translate(calc(var(--random-x3) * 1.5), -400px)
               rotate(var(--random-rotate));
    opacity: 0;
  }
}

.bubble-reset {
  transform: scale(1) translateY(0);
  opacity: 1;
  transition: none;
}
</style>