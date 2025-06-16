// Global variables
let allTransactions = [];
let filteredTransactions = [];
let charts = {};

// API Configuration
const API_BASE = 'http://localhost:5000/api';
const USE_API = false; // Set to true if using Flask API, false for direct database access

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    setupEventListeners();
});

function setupEventListeners() {
    // Modal close
    document.querySelector('.close').onclick = function() {
        document.getElementById('detailModal').style.display = 'none';
    }
    
    // Click outside modal to close
    window.onclick = function(event) {
        const modal = document.getElementById('detailModal');
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
    
    // Search on Enter key
    document.getElementById('searchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchTransactions();
        }
    });
}

async function initializeDashboard() {
    showLoading(true);
    
    try {
        await loadTransactions();
        await loadTransactionTypes();
        updateStatistics();
        createCharts();
        displayTransactions(filteredTransactions);
    } catch (error) {
        console.error('Error initializing dashboard:', error);
        alert('Error loading data. Please check if the database exists and contains data.');
    } finally {
        showLoading(false);
    }
}

async function loadTransactions() {
    if (USE_API) {
        // Use Flask API
        const response = await fetch(`${API_BASE}/transactions`);
        const data = await response.json();
        allTransactions = data.success ? data.data : [];
    } else {
        // Simulate direct database access with sample data
        // In a real implementation, you would load from your SQLite database
        allTransactions = await loadSampleData();
    }
    
    filteredTransactions = [...allTransactions];
}

async function loadSampleData() {
    // This would be replaced with actual database loading in production
    return [
        {
            id: 1,
            transaction_id: 'TXN123456',
            transaction_type: 'Incoming Money',
            amount: 5000,
            fee: 0,
            sender_name: 'John Doe',
            receiver_name: null,
            phone_number: null,
            agent_name: null,
            agent_phone: null,
            date_time: '2024-01-01 10:00:00',
            raw_message: 'You have received 5000 RWF from John Doe. Transaction ID: 123456. Date: 2024-01-01 10:00:00.'
        },
        {
            id: 2,
            transaction_id: 'TXN789012',
            transaction_type: 'Payment Completed',
            amount: 1500,
            fee: 50,
            sender_name: null,
            receiver_name: 'Jane Smith',
            phone_number: null,
            agent_name: null,
            agent_phone: null,
            date_time: '2024-01-02 14:30:00',
            raw_message: 'TxId: 789012. Your payment of 1500 RWF to Jane Smith has been completed. Date: 2024-01-02 14:30:00.'
        },
        {
            id: 3,
            transaction_id: 'TXN345678',
            transaction_type: 'Airtime Payment',
            amount: 3000,
            fee: 50,
            sender_name: null,
            receiver_name: 'Airtime',
            phone_number: null,
            agent_name: null,
            agent_phone: null,
            date_time: '2024-01-03 16:00:00',
            raw_message: '*162*TxId:345678*S*Your payment of 3000 RWF to Airtime has been completed. Fee: 50 RWF. Date: 2024-01-03 16:00:00.'
        }
    ];
}

async function loadTransactionTypes() {
    if (USE_API) {
        const response = await fetch(`${API_BASE}/transaction-types`);
        const data = await response.json();
        const types = data.success ? data.data : [];
        populateTypeFilter(types);
    } else {
        const types = [...new Set(allTransactions.map(t => t.transaction_type))].filter(Boolean);
        populateTypeFilter(types);
    }
}

function populateTypeFilter(types) {
    const select = document.getElementById('typeFilter');
    select.innerHTML = '<option value="">All Transaction Types</option>';
    
    types.forEach(type => {
        const option = document.createElement('option');
        option.value = type;
        option.textContent = type;
        select.appendChild(option);
    });
}

function updateStatistics() {
    const totalTransactions = filteredTransactions.length;
    const totalVolume = filteredTransactions.reduce((sum, t) => sum + (t.amount || 0), 0);
    const totalTypes = new Set(filteredTransactions.map(t => t.transaction_type)).size;
    
    // Calculate this month's transactions
    const currentMonth = new Date().toISOString().substring(0, 7); // YYYY-MM format
    const thisMonth = filteredTransactions.filter(t => 
        t.date_time && t.date_time.substring(0, 7) === currentMonth
    ).length;
    
    document.getElementById('totalTransactions').textContent = totalTransactions.toLocaleString();
    document.getElementById('totalVolume').textContent = `${totalVolume.toLocaleString()} RWF`;
    document.getElementById('totalTypes').textContent = totalTypes;
    document.getElementById('thisMonth').textContent = thisMonth.toLocaleString();
}

function createCharts() {
    createTypeDistributionChart();
    createMonthlyVolumeChart();
}

function createTypeDistributionChart() {
    const ctx = document.getElementById('typeChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (charts.typeChart) {
        charts.typeChart.destroy();
    }
    
    // Calculate type distribution
    const typeData = {};
    filteredTransactions.forEach(t => {
        const type = t.transaction_type || 'Unknown';
        typeData[type] = (typeData[type] || 0) + 1;
    });
    
    const labels = Object.keys(typeData);
    const data = Object.values(typeData);
    const backgroundColors = generateColors(labels.length);
    
    charts.typeChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors,
                borderColor: '#ffd700',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#ffffff',
                        padding: 20
                    }
                }
            }
        }
    });
}

function createMonthlyVolumeChart() {
    const ctx = document.getElementById('monthlyChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (charts.monthlyChart) {
        charts.monthlyChart.destroy();
    }
    
    // Calculate monthly data
    const monthlyData = {};
    filteredTransactions.forEach(t => {
        if (t.date_time) {
            const month = t.date_time.substring(0, 7); // YYYY-MM
            monthlyData[month] = (monthlyData[month] || 0) + (t.amount || 0);
        }
    });
    
    const sortedMonths = Object.keys(monthlyData).sort();
    const volumes = sortedMonths.map(month => monthlyData[month]);
    
    charts.monthlyChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: sortedMonths,
            datasets: [{
                label: 'Monthly Volume (RWF)',
                data: volumes,
                borderColor: '#ffd700',
                backgroundColor: 'rgba(255, 215, 0, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    labels: {
                        color: '#ffffff'
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: '#ffffff'
                    },
                    grid: {
                        color: '#333333'
                    }
                },
                y: {
                    ticks: {
                        color: '#ffffff',
                        callback: function(value) {
                            return value.toLocaleString() + ' RWF';
                        }
                    },
                    grid: {
                        color: '#333333'
                    }
                }
            }
        }
    });
}

function generateColors(count) {
    const colors = [
        '#ffd700', '#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24',
        '#f0932b', '#eb4d4b', '#6c5ce7', '#a29bfe', '#fd79a8',
        '#e17055', '#00b894', '#00cec9', '#0984e3', '#6c5ce7'
    ];
    
    const result = [];
    for (let i = 0; i < count; i++) {
        result.push(colors[i % colors.length]);
    }
    return result;
}

function displayTransactions(transactions) {
    const tbody = document.querySelector('#transactionsTable tbody');
    tbody.innerHTML = '';
    
    if (transactions.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #888;">No transactions found</td></tr>';
        return;
    }
    
    transactions.slice(0, 100).forEach(transaction => { // Limit to first 100 for performance
        const row = document.createElement('tr');
        
        const date = transaction.date_time ? 
            new Date(transaction.date_time).toLocaleDateString() : 'N/A';
        
        const amount = transaction.amount ? 
            `${transaction.amount.toLocaleString()} RWF` : 'N/A';
        
        const details = getTransactionDetails(transaction);
        
        row.innerHTML = `
            <td>${date}</td>
            <td><span class="transaction-type">${transaction.transaction_type || 'Unknown'}</span></td>
            <td><span class="amount">${amount}</span></td>
            <td>${details}</td>
            <td><button class="view-btn" onclick="showTransactionDetail(${transaction.id})">View</button></td>
        `;
        
        tbody.appendChild(row);
    });
}

function getTransactionDetails(transaction) {
    if (transaction.sender_name) {
        return `From: ${transaction.sender_name}`;
    } else if (transaction.receiver_name) {
        return `To: ${transaction.receiver_name}`;
    } else if (transaction.agent_name) {
        return `Agent: ${transaction.agent_name}`;
    } else {
        return transaction.transaction_id || 'N/A';
    }
}

function showTransactionDetail(transactionId) {
    const transaction = allTransactions.find(t => t.id === transactionId);
    if (!transaction) return;
    
    const modalContent = document.getElementById('modalContent');
    modalContent.innerHTML = `
        <div class="detail-item">
            <div class="detail-label">Transaction ID</div>
            <div class="detail-value">${transaction.transaction_id || 'N/A'}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Type</div>
            <div class="detail-value">${transaction.transaction_type || 'Unknown'}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Amount</div>
            <div class="detail-value">${transaction.amount ? transaction.amount.toLocaleString() + ' RWF' : 'N/A'}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Fee</div>
            <div class="detail-value">${transaction.fee ? transaction.fee.toLocaleString() + ' RWF' : '0 RWF'}</div>
        </div>
        <div class="detail-item">
            <div class="detail-label">Date & Time</div>
            <div class="detail-value">${transaction.date_time ? new Date(transaction.date_time).toLocaleString() : 'N/A'}</div>
        </div>
        ${transaction.sender_name ? `
        <div class="detail-item">
            <div class="detail-label">From</div>
            <div class="detail-value">${transaction.sender_name}</div>
        </div>` : ''}
        ${transaction.receiver_name ? `
        <div class="detail-item">
            <div class="detail-label">To</div>
            <div class="detail-value">${transaction.receiver_name}</div>
        </div>` : ''}
        ${transaction.agent_name ? `
        <div class="detail-item">
            <div class="detail-label">Agent</div>
            <div class="detail-value">${transaction.agent_name} (${transaction.agent_phone || 'N/A'})</div>
        </div>` : ''}
        <div class="detail-item">
            <div class="detail-label">Original Message</div>
            <div class="detail-value" style="font-style: italic; background: #1a1a1a; padding: 10px; border-radius: 5px;">${transaction.raw_message || 'N/A'}</div>
        </div>
    `;
    
    document.getElementById('detailModal').style.display = 'block';
}

function searchTransactions() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase().trim();
    
    if (searchTerm === '') {
        filteredTransactions = [...allTransactions];
    } else {
        filteredTransactions = allTransactions.filter(transaction => {
            return (
                (transaction.raw_message && transaction.raw_message.toLowerCase().includes(searchTerm)) ||
                (transaction.transaction_type && transaction.transaction_type.toLowerCase().includes(searchTerm)) ||
                (transaction.sender_name && transaction.sender_name.toLowerCase().includes(searchTerm)) ||
                (transaction.receiver_name && transaction.receiver_name.toLowerCase().includes(searchTerm)) ||
                (transaction.transaction_id && transaction.transaction_id.toLowerCase().includes(searchTerm))
            );
        });
    }
    
    updateDashboard();
}

function filterTransactions() {
    const selectedType = document.getElementById('typeFilter').value;
    
    if (selectedType === '') {
        filteredTransactions = [...allTransactions];
    } else {
        filteredTransactions = allTransactions.filter(transaction => 
            transaction.transaction_type === selectedType
        );
    }
    
    updateDashboard();
}

function clearFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('typeFilter').value = '';
    filteredTransactions = [...allTransactions];
    updateDashboard();
}

function updateDashboard() {
    updateStatistics();
    createCharts();
    displayTransactions(filteredTransactions);
}

function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}
