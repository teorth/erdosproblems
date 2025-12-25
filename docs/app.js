/**
 * Main Application Logic for Erdos Problems Interactive Table
 * Coordinates data loading, rendering, sorting, and filtering
 */

// Global state
let allProblems = [];
let filteredProblems = [];
let currentSort = { column: 'number', direction: 'asc' };

/**
 * Load problems from YAML file
 * @returns {Promise<Array<Object>>} Array of problem objects
 */
async function loadProblems() {
    try {
        const rawYamlUrl = 'https://raw.githubusercontent.com/teorth/erdosproblems/main/data/problems.yaml';
        const response = await fetch(rawYamlUrl);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const yamlText = await response.text();
        const problems = jsyaml.load(yamlText);

        if (!Array.isArray(problems)) {
            throw new Error('Invalid YAML format: expected array of problems');
        }

        return problems;
    } catch (error) {
        console.error('Error loading problems:', error);
        showError('Failed to load problems data. Please try refreshing the page.');
        return [];
    }
}

/**
 * Display error message to user
 * @param {string} message - Error message to display
 */
function showError(message) {
    const tableBody = document.getElementById('table-body');
    if (tableBody) {
        tableBody.innerHTML = `<tr><td colspan="7" class="loading-cell" style="color: red;">${escapeHtml(message)}</td></tr>`;
    }
}

/**
 * Sort problems by column
 * @param {Array<Object>} problems - Array of problems to sort
 * @param {string} column - Column name to sort by
 * @param {string} direction - Sort direction ('asc' or 'desc')
 * @returns {Array<Object>} Sorted array of problems
 */
function sortProblems(problems, column, direction) {
    return [...problems].sort((a, b) => {
        let valA = getColumnValue(a, column);
        let valB = getColumnValue(b, column);

        // Handle numeric sorting for 'number' column
        if (column === 'number') {
            valA = parseInt(valA, 10) || 0;
            valB = parseInt(valB, 10) || 0;
        }

        // Handle prize amount sorting
        if (column === 'prize') {
            valA = parsePrize(valA);
            valB = parsePrize(valB);
        }

        // String comparison for other columns
        if (typeof valA === 'string') {
            valA = valA.toLowerCase();
        }
        if (typeof valB === 'string') {
            valB = valB.toLowerCase();
        }

        // Compare values
        let comparison = 0;
        if (valA > valB) {
            comparison = 1;
        } else if (valA < valB) {
            comparison = -1;
        }

        return direction === 'asc' ? comparison : -comparison;
    });
}

/**
 * Render table with problems data
 * @param {Array<Object>} problems - Array of problems to render
 */
function renderTable(problems) {
    const tableBody = document.getElementById('table-body');
    if (!tableBody) return;

    if (problems.length === 0) {
        tableBody.innerHTML = '<tr><td colspan="7" class="loading-cell">No problems match the current filters.</td></tr>';
        return;
    }

    // Build table rows
    const rows = problems.map(problem => {
        const number = problem.number || '';
        const prize = problem.prize || 'no';
        const status = problem.status || {};
        const formalized = problem.formalized || {};
        const oeis = problem.oeis || [];
        const tags = problem.tags || [];
        const comments = problem.comments || '';

        return `
            <tr>
                <td>${renderProblemLink(number)}</td>
                <td>${renderPrize(prize)}</td>
                <td>${renderStatus(status)}</td>
                <td>${renderFormalizedLink(number, formalized.state)}</td>
                <td>${renderOEISLinks(oeis)}</td>
                <td>${renderTags(tags)}</td>
                <td>${renderComments(comments)}</td>
            </tr>
        `;
    }).join('');

    tableBody.innerHTML = rows;

    // Update stats
    updateStats(problems.length, allProblems.length);
}

/**
 * Update statistics display
 * @param {number} showing - Number of problems currently shown
 * @param {number} total - Total number of problems
 */
function updateStats(showing, total) {
    const showingCount = document.getElementById('showing-count');
    if (showingCount) {
        showingCount.textContent = `Showing ${showing.toLocaleString()} of ${total.toLocaleString()} problems`;
    }
}

/**
 * Handle sort header click
 * @param {Event} event - Click event
 */
function handleSortClick(event) {
    const header = event.currentTarget;
    const column = header.getAttribute('data-sort');

    if (!column) return;

    // Toggle direction if clicking same column, otherwise default to asc
    if (currentSort.column === column) {
        currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort.column = column;
        currentSort.direction = 'asc';
    }

    // Update visual indicators
    updateSortIndicators(currentSort.column, currentSort.direction);

    // Re-render table
    updateTable();

    // Save state to URL
    saveStateToURL(getCurrentState());
}

/**
 * Update table with current filters and sort
 */
function updateTable() {
    const searchBox = document.getElementById('search-box');
    const searchQuery = searchBox ? searchBox.value : '';

    // Apply search
    let results = searchProblems(allProblems, searchQuery);

    // Apply filters
    const filters = getCurrentFilters();
    results = applyFilters(results, filters);

    // Apply sort
    results = sortProblems(results, currentSort.column, currentSort.direction);

    // Store filtered results
    filteredProblems = results;

    // Render
    renderTable(results);

    // Save state to URL
    saveStateToURL(getCurrentState());
}

/**
 * Initialize sort event listeners
 */
function initializeSortListeners() {
    document.querySelectorAll('th.sortable').forEach(header => {
        header.addEventListener('click', handleSortClick);
    });
}

/**
 * Initialize the application
 */
async function initialize() {
    // Show loading indicator
    const loadingIndicator = document.getElementById('loading-indicator');
    if (loadingIndicator) {
        loadingIndicator.style.display = 'inline';
    }

    // Load problems data
    allProblems = await loadProblems();

    if (allProblems.length === 0) {
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
        return;
    }

    // Extract and populate tags
    const allTags = extractAllTags(allProblems);
    populateTagFilters(allTags);

    // Load state from URL
    const urlState = loadStateFromURL();
    currentSort.column = urlState.sortColumn;
    currentSort.direction = urlState.sortDirection;

    // Restore UI state
    restoreUIState(urlState);

    // Initialize event listeners
    initializeSortListeners();
    initializeFilterListeners();

    // Set filter change handler
    setFilterChangeHandler(updateTable);

    // Initial render
    updateTable();

    // Hide loading indicator
    if (loadingIndicator) {
        loadingIndicator.style.display = 'none';
    }

    console.log(`Loaded ${allProblems.length} problems successfully`);
}

// Start the application when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
} else {
    initialize();
}
