<script setup lang="ts">
import Scoreboard from "./views/Scoreboard.vue";
import './assets/theme.css';
</script>

<style>
.app-container {
    min-height: 100vh;
    background: 
        linear-gradient(to bottom, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.8)),
        linear-gradient(90deg, rgba(0, 255, 255, 0.1) 1px, transparent 1px) 0 0 / 20px 20px,
        linear-gradient(rgba(0, 255, 255, 0.1) 1px, transparent 1px) 0 0 / 20px 20px,
        url('/src/assets/background.jpg');
    background-size: auto, 20px 20px, 20px 20px, cover;
    background-position: center;
    background-color: #000912;
}

@keyframes scroll {
    0% {
        background-position: 0 0, 0 0, 0 0;
    }
    100% {
        background-position: 0 100vh, 20px 20px, 20px 20px;
    }
}

body {
    margin: 0;
    padding: 0;
    overflow-x: hidden;
}

* {
    box-sizing: border-box;
}
</style>

<template>
    <div class="app-container">
        <Scoreboard />
    </div>
</template>