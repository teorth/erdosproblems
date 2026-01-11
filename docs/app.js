/**
 * Main Application Logic for Erdos Problems Interactive Table
 * Coordinates data loading, rendering, sorting, and filtering
 */

// Global state
let allProblems = [];
let filteredProblems = [];
let currentSort = { column: 'number', direction: 'asc' };

// Pagination
const DEFAULT_PAGE_SIZE = 100;
let currentPage = 1;
let pageSize = DEFAULT_PAGE_SIZE;

function getPageSizeFromUI() {
    const input = document.getElementById('page-size');
    if (!input) return pageSize;

    // Keep the last valid value while the user is typing.
    const value = input.value.trim();
    if (!/^[1-9]\d*$/.test(value)) return pageSize;

    // Regex guarantees a positive integer.
    return Number(value);
}

function setPageSizeInUI(size) {
    const input = document.getElementById('page-size');
    if (!input) return;
    input.value = String(size);
}

function resetToFirstPageAndUpdate() {
    currentPage = 1;
    updateTable();
}

function updatePaginationUI(totalPages) {
    const info = document.getElementById('pagination-info');
    const prevBtn = document.getElementById('pagination-prev');
    const nextBtn = document.getElementById('pagination-next');

    if (info) {
        info.textContent = `Page ${currentPage.toLocaleString()} / ${totalPages.toLocaleString()}`;
    }
    if (prevBtn) {
        prevBtn.disabled = currentPage <= 1;
    }
    if (nextBtn) {
        nextBtn.disabled = currentPage >= totalPages;
    }
}

function initializePaginationListeners() {
    const prevBtn = document.getElementById('pagination-prev');
    const nextBtn = document.getElementById('pagination-next');
    const pageSizeInput = document.getElementById('page-size');

    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            currentPage = Math.max(1, currentPage - 1);
            updateTable();
        });
    }

    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            currentPage += 1;
            updateTable();
        });
    }

    if (pageSizeInput) {
        let inputTimeout;

        const applyPageSize = () => {
            const newSize = getPageSizeFromUI();
            pageSize = newSize;
            // Changing page size should reset to page 1
            currentPage = 1;
            updateTable(); // updateTable will save state to URL
        };

        // Update as the user types, but debounce so we don't re-render on every keystroke.
        pageSizeInput.addEventListener('input', () => {
            clearTimeout(inputTimeout);
            inputTimeout = setTimeout(applyPageSize, 250);
        });

        // Commit immediately on blur/enter (change fires on commit)
        pageSizeInput.addEventListener('change', () => {
            clearTimeout(inputTimeout);
            applyPageSize();
        });
    }
}

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
        // With pagination, show filtered vs total(allProblems.length) counts (range is empty here)
        updateStats();
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
    updateStats();
}

/**
 * Update statistics display
 */
function updateStats() {
    const showingCount = document.getElementById('showing-count');
    if (showingCount) {
        const filteredTotal = Array.isArray(filteredProblems) ? filteredProblems.length : 0;
        const start = filteredTotal === 0 ? 0 : ((currentPage - 1) * pageSize + 1);
        const end = filteredTotal === 0 ? 0 : Math.min(currentPage * pageSize, filteredTotal);

        // N.B: total = allProblems.length i.e total number of problems
        // Example: "Showing 201–300 of 1,742 (total 2,100) problems"
        // When no filters are active, filteredTotal === total.
        if (filteredTotal > 0) {
            showingCount.textContent = `Showing ${start.toLocaleString()}–${end.toLocaleString()} of ${filteredTotal.toLocaleString()} (total ${allProblems.length.toLocaleString()}) problems`;
        } else {
            showingCount.textContent = `Showing 0 of 0 (total ${allProblems.length.toLocaleString()}) problems`;
        }
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

    // Sorting should reset pagination
    currentPage = 1;

    // Re-render table
    updateTable();
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

    // Pagination: slice the final, sorted results
    pageSize = getPageSizeFromUI();
    const totalPages = Math.max(1, Math.ceil(results.length / pageSize));
    if (!Number.isFinite(currentPage) || currentPage < 1) currentPage = 1;
    if (currentPage > totalPages) currentPage = totalPages;
    const startIndex = (currentPage - 1) * pageSize;
    const pagedResults = results.slice(startIndex, startIndex + pageSize);

    // Update tag and dropdown displays with filtered counts
    const nonTagFiltersActive = hasNonTagFilters();

    // Update tag display (excludes tag filters from count calculation)
    if (nonTagFiltersActive) {
        window._filteredTagCounts = extractTagCounts(filteredProblems);
        window._hasActiveFilters = true;
    } else {
        window._filteredTagCounts = null;
        window._hasActiveFilters = false;
    }

    // Trigger tag re-sort with current sort preference to apply two-tier sorting
    const tagSortAlpha = document.getElementById('tag-sort-alpha');
    const currentTagSort = tagSortAlpha && tagSortAlpha.checked ? 'alpha' : 'count';
    resortTagFilters(currentTagSort);

    // Update dropdown displays (each dropdown excludes its own filter from count calculation)
    const hasAnyFilters = nonTagFiltersActive || (filters.tags && filters.tags.length > 0);
    updateAllDropdownDisplays(allProblems, hasAnyFilters);

    // Render
    renderTable(pagedResults);

    // Update pagination controls
    updatePaginationUI(totalPages);

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

    // Update header and meta description with actual problem count
    const problemCount = allProblems.length.toLocaleString();
    const headerSubtitle = document.getElementById('header-subtitle');
    if (headerSubtitle) {
        headerSubtitle.textContent = `Interactive table of ${problemCount} mathematical problems`;
    }
    const metaDescription = document.getElementById('meta-description');
    if (metaDescription) {
        metaDescription.setAttribute('content', `Interactive table of ${problemCount} mathematical problems from the Erdős problem database`);
    }

    // Set filter change handler FIRST (before creating any event listeners)
    // Any query change should reset pagination.
    setFilterChangeHandler(resetToFirstPageAndUpdate);

    // Extract tag counts and tags
    const tagCounts = extractTagCounts(allProblems);

    // Store globally for tag sort functionality
    window._allProblems = allProblems;
    window._tagCounts = tagCounts;
    window._filteredTagCounts = null;
    window._hasActiveFilters = false;

    // Store original dropdown option text
    ['filter-status', 'filter-prize', 'filter-formalized', 'filter-oeis'].forEach(selectId => {
        const select = document.getElementById(selectId);
        if (select) {
            const options = select.querySelectorAll('option:not([value=""])');
            options.forEach(option => {
                option.setAttribute('data-original', option.textContent);
            });
        }
    });

    // Load state from URL
    const urlState = loadStateFromURL();
    currentSort.column = urlState.sortColumn;
    currentSort.direction = urlState.sortDirection;

    // Restore pagination from URL
    currentPage = urlState.page || 1;
    pageSize = urlState.pageSize || DEFAULT_PAGE_SIZE;
    setPageSizeInUI(pageSize);

    // Get initial tag sort preference from URL
    const initialTagSort = urlState.tagSort || 'count';

    // Extract and populate tags with initial sort
    const allTags = extractAllTags(allProblems, initialTagSort, tagCounts);
    populateTagFilters(allTags, tagCounts);

    // Restore UI state
    restoreUIState(urlState);

    // Initialize event listeners
    initializeSortListeners();
    initializeFilterListeners();
    initializePaginationListeners();

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
