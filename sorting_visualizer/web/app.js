const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

const algorithmSelect = document.getElementById("algorithm");
const sizeInput = document.getElementById("size");
const speedInput = document.getElementById("speed");
const minValueInput = document.getElementById("minValue");
const maxValueInput = document.getElementById("maxValue");

const sizeValue = document.getElementById("sizeValue");
const speedValue = document.getElementById("speedValue");

const statAlgorithm = document.getElementById("statAlgorithm");
const statSize = document.getElementById("statSize");
const statSpeed = document.getElementById("statSpeed");

const comparisonsEl = document.getElementById("comparisons");
const swapsEl = document.getElementById("swaps");
const elapsedEl = document.getElementById("elapsed");

const startButton = document.getElementById("start");
const stopButton = document.getElementById("stop");
const randomizeButton = document.getElementById("randomize");
const exportButton = document.getElementById("export");

let data = [];
let stopRequested = false;
let comparisons = 0;
let swaps = 0;
let startTime = 0;

function updateStats() {
  statAlgorithm.textContent = algorithmSelect.value;
  statSize.textContent = sizeInput.value;
  statSpeed.textContent = `${speedInput.value} ms`;
  comparisonsEl.textContent = comparisons;
  swapsEl.textContent = swaps;
  if (startTime) {
    const seconds = (performance.now() - startTime) / 1000;
    elapsedEl.textContent = `${seconds.toFixed(2)} s`;
  }
}

function resetMetrics() {
  comparisons = 0;
  swaps = 0;
  startTime = 0;
  elapsedEl.textContent = "0.00 s";
  updateStats();
}

function randomArray() {
  const size = Number(sizeInput.value);
  const min = Number(minValueInput.value);
  const max = Number(maxValueInput.value);
  const safeMin = Math.min(min, max - 1);
  data = Array.from({ length: size }, () =>
    Math.floor(Math.random() * (max - safeMin + 1)) + safeMin
  );
  drawArray();
}

function drawArray({ highlight = [], swapped = [], sorted = [] } = {}) {
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;
  ctx.clearRect(0, 0, width, height);

  const barWidth = width / data.length;
  const maxValue = Math.max(...data, 1);

  data.forEach((value, i) => {
    const barHeight = (value / maxValue) * (height - 10);
    let color = "#93c5fd";
    if (sorted.includes(i)) color = "#06d6a0";
    if (highlight.includes(i)) color = "#ff6b6b";
    if (swapped.includes(i)) color = "#ffd166";

    ctx.fillStyle = color;
    ctx.fillRect(i * barWidth, height - barHeight, barWidth - 1, barHeight);
  });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function bubbleSort() {
  const sortedIndices = [];
  for (let i = 0; i < data.length; i += 1) {
    for (let j = 0; j < data.length - i - 1; j += 1) {
      if (stopRequested) return;
      comparisons += 1;
      drawArray({ highlight: [j, j + 1], sorted: sortedIndices });
      updateStats();
      await sleep(Number(speedInput.value));
      if (data[j] > data[j + 1]) {
        swaps += 1;
        [data[j], data[j + 1]] = [data[j + 1], data[j]];
        drawArray({ swapped: [j, j + 1], sorted: sortedIndices });
        updateStats();
        await sleep(Number(speedInput.value));
      }
    }
    sortedIndices.push(data.length - i - 1);
  }
  drawArray({ sorted: sortedIndices });
}

async function quickSort(left, right, sortedIndices) {
  if (stopRequested) return;
  if (left >= right) {
    if (left === right) sortedIndices.add(left);
    return;
  }

  const pivot = data[right];
  let i = left;

  for (let j = left; j < right; j += 1) {
    if (stopRequested) return;
    comparisons += 1;
    drawArray({ highlight: [j, right], sorted: Array.from(sortedIndices) });
    updateStats();
    await sleep(Number(speedInput.value));
    if (data[j] < pivot) {
      swaps += 1;
      [data[i], data[j]] = [data[j], data[i]];
      drawArray({ swapped: [i, j], sorted: Array.from(sortedIndices) });
      updateStats();
      await sleep(Number(speedInput.value));
      i += 1;
    }
  }

  swaps += 1;
  [data[i], data[right]] = [data[right], data[i]];
  sortedIndices.add(i);
  drawArray({ swapped: [i, right], sorted: Array.from(sortedIndices) });
  updateStats();
  await sleep(Number(speedInput.value));

  await quickSort(left, i - 1, sortedIndices);
  await quickSort(i + 1, right, sortedIndices);
}

async function mergeSort(left, right, sortedIndices) {
  if (stopRequested) return;
  if (left >= right) {
    if (left === right) sortedIndices.add(left);
    return;
  }

  const mid = Math.floor((left + right) / 2);
  await mergeSort(left, mid, sortedIndices);
  await mergeSort(mid + 1, right, sortedIndices);

  const leftArr = data.slice(left, mid + 1);
  const rightArr = data.slice(mid + 1, right + 1);

  let i = 0;
  let j = 0;
  let k = left;

  while (i < leftArr.length && j < rightArr.length) {
    if (stopRequested) return;
    comparisons += 1;
    drawArray({ highlight: [k], sorted: Array.from(sortedIndices) });
    updateStats();
    await sleep(Number(speedInput.value));

    if (leftArr[i] <= rightArr[j]) {
      data[k] = leftArr[i];
      i += 1;
    } else {
      data[k] = rightArr[j];
      j += 1;
    }
    swaps += 1;
    k += 1;
  }

  while (i < leftArr.length) {
    if (stopRequested) return;
    data[k] = leftArr[i];
    i += 1;
    k += 1;
  }

  while (j < rightArr.length) {
    if (stopRequested) return;
    data[k] = rightArr[j];
    j += 1;
    k += 1;
  }

  if (right - left < 6) {
    for (let idx = left; idx <= right; idx += 1) {
      sortedIndices.add(idx);
    }
  }
  drawArray({ sorted: Array.from(sortedIndices) });
  updateStats();
  await sleep(Number(speedInput.value));
}

async function startSorting() {
  stopRequested = false;
  resetMetrics();
  startTime = performance.now();
  updateStats();

  const min = Number(minValueInput.value);
  const max = Number(maxValueInput.value);
  if (Number.isNaN(min) || Number.isNaN(max) || max <= min) {
    alert("Please set a valid value range (max must be greater than min).");
    return;
  }

  if (!data.length) randomArray();

  const algorithm = algorithmSelect.value;
  if (algorithm === "Bubble Sort") {
    await bubbleSort();
  } else if (algorithm === "Quick Sort") {
    const sortedIndices = new Set();
    await quickSort(0, data.length - 1, sortedIndices);
    drawArray({ sorted: Array.from(sortedIndices) });
  } else {
    const sortedIndices = new Set();
    await mergeSort(0, data.length - 1, sortedIndices);
    drawArray({ sorted: Array.from(sortedIndices) });
  }

  updateStats();
}

function stopSorting() {
  stopRequested = true;
}

function resizeCanvas() {
  const { width } = canvas.getBoundingClientRect();
  const ratio = window.devicePixelRatio || 1;
  canvas.width = Math.floor(width * ratio);
  canvas.height = Math.floor(420 * ratio);
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  canvas.style.height = "420px";
  drawArray();
}

sizeInput.addEventListener("input", () => {
  sizeValue.textContent = sizeInput.value;
  statSize.textContent = sizeInput.value;
});

speedInput.addEventListener("input", () => {
  speedValue.textContent = speedInput.value;
  statSpeed.textContent = `${speedInput.value} ms`;
});

algorithmSelect.addEventListener("change", updateStats);
randomizeButton.addEventListener("click", () => {
  stopSorting();
  randomArray();
});
startButton.addEventListener("click", startSorting);
stopButton.addEventListener("click", stopSorting);
exportButton.addEventListener("click", () => {
  const link = document.createElement("a");
  link.download = `sorting-visualizer-${algorithmSelect.value.replace(/\\s+/g, "-").toLowerCase()}.png`;
  link.href = canvas.toDataURL("image/png");
  link.click();
});

window.addEventListener("resize", resizeCanvas);

sizeValue.textContent = sizeInput.value;
speedValue.textContent = speedInput.value;
updateStats();
resizeCanvas();
randomArray();
