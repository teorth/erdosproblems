/**
 * Filter Logic Module
 * Handles search and filtering of problems
 */

/**
 * Search problems by text query across all fields
 * @param {Array<Object>} problems - Array of problem objects
 * @param {string} query - Search query string
 * @returns {Array<Object>} Filtered array of problems
 */
function searchProblems(problems, query) {
    if (!query || query.trim() === '') {
        return problems;
    }

    const searchTerm = query.toLowerCase().trim();

    return problems.filter(problem => {
        // Build searchable text from all fields
        const searchableFields = [
            problem.number || '',
            problem.prize || '',
            (problem.status && problem.status.state) || '',
            (problem.status && problem.status.note) || '',
            (problem.formalized && problem.formalized.state) || '',
            (problem.formalized && problem.formalized.note) || '',
            (problem.oeis && Array.isArray(problem.oeis)) ? problem.oeis.join(' ') : '',
            (problem.tags && Array.isArray(problem.tags)) ? problem.tags.join(' ') : '',
            problem.comments || ''
        ];

        const searchableText = searchableFields.join(' ').toLowerCase();
        return searchableText.includes(searchTerm);
    });
}

/**
 * Apply all filters to problems array
 * @param {Array<Object>} problems - Array of problem objects
 * @param {Object} filters - Filter criteria
 * @param {string} filters.status - Status filter value
 * @param {string} filters.prize - Prize filter value ('yes' or 'no')
 * @param {string} filters.formalized - Formalized filter value ('yes' or 'no')
 * @param {Array<string>} filters.tags - Array of selected tag values (OR logic)
 * @returns {Array<Object>} Filtered array of problems
 */
function applyFilters(problems, filters) {
    return problems.filter(problem => {
        // Status filter
        if (filters.status && filters.status !== '') {
            const problemStatus = (problem.status && problem.status.state) || '';
            if (problemStatus !== filters.status) {
                return false;
            }
        }

        // Prize filter
        if (filters.prize && filters.prize !== '') {
            const hasPrize = problem.prize && problem.prize !== 'no';
            if (filters.prize === 'yes' && !hasPrize) {
                return false;
            }
            if (filters.prize === 'no' && hasPrize) {
                return false;
            }
        }

        // Formalized filter
        if (filters.formalized && filters.formalized !== '') {
            const formalizedState = (problem.formalized && problem.formalized.state) || 'no';
            if (formalizedState !== filters.formalized) {
                return false;
            }
        }

        // Tags filter (OR logic - problem must have at least one selected tag)
        if (filters.tags && filters.tags.length > 0) {
            const problemTags = problem.tags || [];
            const hasAnyTag = filters.tags.some(tag => problemTags.includes(tag));
            if (!hasAnyTag) {
                return false;
            }
        }

        return true;
    });
}

/**
 * Populate tag filter checkboxes
 * @param {Array<string>} allTags - Sorted array of all unique tags
 */
function populateTagFilters(allTags) {
    const container = document.getElementById('tags-checkboxes');
    if (!container) return;

    container.innerHTML = ''; // Clear existing

    allTags.forEach(tag => {
        // Create container div
        const itemDiv = document.createElement('div');
        itemDiv.className = 'tag-checkbox-item';

        // Create checkbox
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = `tag-${sanitizeTagId(tag)}`;
        checkbox.value = tag;
        checkbox.className = 'tag-filter-checkbox';

        // Create label
        const label = document.createElement('label');
        label.htmlFor = checkbox.id;
        label.textContent = tag;

        // Append to container
        itemDiv.appendChild(checkbox);
        itemDiv.appendChild(label);
        container.appendChild(itemDiv);

        // Add event listener for filter change
        checkbox.addEventListener('change', handleFilterChange);
    });
}

/**
 * Filter tag checkboxes based on search query
 * @param {string} searchQuery - Search query for tags
 */
function filterTagCheckboxes(searchQuery) {
    const query = searchQuery.toLowerCase().trim();
    const items = document.querySelectorAll('.tag-checkbox-item');

    items.forEach(item => {
        const label = item.querySelector('label');
        const tagName = label.textContent.toLowerCase();
        const matches = query === '' || tagName.includes(query);
        item.style.display = matches ? 'flex' : 'none';
    });
}

/**
 * Get current filter values from UI
 * @returns {Object} Current filter state
 */
function getCurrentFilters() {
    const statusFilter = document.getElementById('filter-status');
    const prizeFilter = document.getElementById('filter-prize');
    const formalizedFilter = document.getElementById('filter-formalized');

    // Get selected tags
    const selectedTags = [];
    document.querySelectorAll('.tag-filter-checkbox:checked').forEach(checkbox => {
        selectedTags.push(checkbox.value);
    });

    return {
        status: statusFilter ? statusFilter.value : '',
        prize: prizeFilter ? prizeFilter.value : '',
        formalized: formalizedFilter ? formalizedFilter.value : '',
        tags: selectedTags
    };
}

/**
 * Reset all filters to default values
 */
function resetAllFilters() {
    // Reset search box
    const searchBox = document.getElementById('search-box');
    if (searchBox) {
        searchBox.value = '';
    }

    // Reset filter dropdowns
    const statusFilter = document.getElementById('filter-status');
    if (statusFilter) {
        statusFilter.value = '';
    }

    const prizeFilter = document.getElementById('filter-prize');
    if (prizeFilter) {
        prizeFilter.value = '';
    }

    const formalizedFilter = document.getElementById('filter-formalized');
    if (formalizedFilter) {
        formalizedFilter.value = '';
    }

    // Reset tag checkboxes
    document.querySelectorAll('.tag-filter-checkbox').forEach(checkbox => {
        checkbox.checked = false;
    });

    // Reset tag search
    const tagSearch = document.getElementById('tag-search');
    if (tagSearch) {
        tagSearch.value = '';
        filterTagCheckboxes('');
    }

    // Trigger filter change
    handleFilterChange();
}

/**
 * Handle filter change event
 * This function will be set by app.js to update the table
 */
let handleFilterChange = function() {
    console.log('Filter change handler not yet initialized');
};

/**
 * Set the filter change handler
 * @param {Function} handler - Function to call when filters change
 */
function setFilterChangeHandler(handler) {
    handleFilterChange = handler;
}

/**
 * Initialize filter event listeners
 */
function initializeFilterListeners() {
    // Search box
    const searchBox = document.getElementById('search-box');
    if (searchBox) {
        // Debounce search input
        let searchTimeout;
        searchBox.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                handleFilterChange();
            }, 300); // 300ms debounce
        });
    }

    // Filter dropdowns
    const statusFilter = document.getElementById('filter-status');
    if (statusFilter) {
        statusFilter.addEventListener('change', handleFilterChange);
    }

    const prizeFilter = document.getElementById('filter-prize');
    if (prizeFilter) {
        prizeFilter.addEventListener('change', handleFilterChange);
    }

    const formalizedFilter = document.getElementById('filter-formalized');
    if (formalizedFilter) {
        formalizedFilter.addEventListener('change', handleFilterChange);
    }

    // Reset button
    const resetButton = document.getElementById('reset-filters');
    if (resetButton) {
        resetButton.addEventListener('click', resetAllFilters);
    }

    // Tag search box
    const tagSearch = document.getElementById('tag-search');
    if (tagSearch) {
        tagSearch.addEventListener('input', (e) => {
            filterTagCheckboxes(e.target.value);
        });
    }
}
