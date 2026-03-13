// ========== КОНФИГУРАЦИЯ ==========
const API_BASE_URL = 'http://192.168.0.109:8000/api';
let currentSensorId = null;
let currentHours = 24;
let myChart = null;
let autoRefreshInterval = null;

// ========== ИНИЦИАЛИЗАЦИЯ ==========
document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Prometeo Dashboard загружен');

    // Инициализация Chart.js
    initChart();

    // Загрузка списка датчиков
    await loadSensors();

    // Обработчики событий
    setupEventListeners();

    // Автообновление каждые 30 секунд
    startAutoRefresh(30000);

    console.log('✅ Инициализация завершена');
});

// ========== ИНИЦИАЛИЗАЦИЯ ГРАФИКА ==========
function initChart() {
    const ctx = document.getElementById('timeseriesChart').getContext('2d');
    myChart = new Chart(ctx, chartConfig);
    console.log('📊 График инициализирован');
}

// ========== ЗАГРУЗКА СПИСКА ДАТЧИКОВ ==========
async function loadSensors() {
    try {
        updateConnectionStatus('loading');

        const response = await fetch(`${API_BASE_URL}/sensors`);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();
        const sensors = data.sensors;

        const selectElement = document.getElementById('sensorSelect');
        selectElement.innerHTML = '<option value="">-- Выберите датчик --</option>';

        sensors.forEach(sensor => {
            const option = document.createElement('option');
            option.value = sensor.id;
            option.textContent = `${sensor.name} (${sensor.location})`;
            selectElement.appendChild(option);
        });

        // Автоматически выбираем первый датчик
        if (sensors.length > 0) {
            selectElement.value = sensors[0].id;
            currentSensorId = sensors[0].id;
            await loadSensorData();
        }

        updateConnectionStatus('connected');
        console.log(`✅ Загружено ${sensors.length} датчиков`);

    } catch (error) {
        console.error('❌ Ошибка загрузки датчиков:', error);
        updateConnectionStatus('error');
        showNotification('Ошибка подключения к API', 'error');
    }
}

// ========== ЗАГРУЗКА ДАННЫХ ДАТЧИКА ==========
async function loadSensorData() {
    if (!currentSensorId) {
        console.warn('⚠️ Датчик не выбран');
        return;
    }

    try {
        // Параллельная загрузка статистики и временного ряда
        const [statsResponse, timeseriesResponse] = await Promise.all([
            fetch(`${API_BASE_URL}/stats/${currentSensorId}?hours=${currentHours}`),
            fetch(`${API_BASE_URL}/timeseries/${currentSensorId}?hours=${currentHours}&interval=5`)
        ]);

        if (!statsResponse.ok || !timeseriesResponse.ok) {
            throw new Error('Ошибка получения данных');
        }

        const stats = await statsResponse.json();
        const timeseriesData = await timeseriesResponse.json();
