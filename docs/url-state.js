/**
 * URL State Persistence Module
 * Handles encoding/decoding filter and sort state to/from URL query parameters
 */

/**
 * Save current state to URL query parameters
 * @param {Object} state - Current application state
 * @param {string} state.sortColumn - Column to sort by
 * @param {string} state.sortDirection - Sort direction ('asc' or 'desc')
 * @param {string} state.search - Search query
 * @param {string} state.statusFilter - Status filter value
 * @param {string} state.prizeFilter - Prize filter value
 * @param {string} state.formalizedFilter - Formalized filter value
 * @param {string} state.oeisFilter - OEIS filter value
 * @param {Array<string>} state.selectedTags - Array of selected tag values
 * @param {string} state.tagLogic - Tag logic ('any' or 'all')
 */
function saveStateToURL(state) {
    const params = new URLSearchParams();

    // Only add non-default values to keep URL clean
    if (state.sortColumn && state.sortColumn !== 'number') {
        params.set('sort', state.sortColumn);
    }

    if (state.sortDirection && state.sortDirection !== 'asc') {
        params.set('dir', state.sortDirection);
    }

    if (state.search && state.search.trim() !== '') {
        params.set('q', state.search.trim());
    }

    if (state.statusFilter && state.statusFilter !== '') {
        params.set('status', state.statusFilter);
    }

    if (state.prizeFilter && state.prizeFilter !== '') {
        params.set('prize', state.prizeFilter);
    }

    if (state.formalizedFilter && state.formalizedFilter !== '') {
        params.set('formalized', state.formalizedFilter);
    }

    if (state.oeisFilter && state.oeisFilter !== '') {
        params.set('oeis', state.oeisFilter);
    }

    if (state.selectedTags && state.selectedTags.length > 0) {
        params.set('tags', state.selectedTags.join(','));
    }

    if (state.tagLogic && state.tagLogic !== 'any') {
        params.set('tagLogic', state.tagLogic);
    }

    if (state.tagSort && state.tagSort !== 'count') {
        params.set('tagSort', state.tagSort);
    }

    // Pagination
    if (state.page && state.page !== 1) {
        params.set('page', String(state.page));
    }

    if (state.pageSize && state.pageSize !== 100) {
        params.set('pageSize', String(state.pageSize));
    }

    // Update URL without reload using History API
    const queryString = params.toString();
    const newURL = queryString
        ? `${window.location.pathname}?${queryString}`
        : window.location.pathname;

    window.history.replaceState(null, '', newURL);
}

/**
 * Load state from URL query parameters
 * @returns {Object} State object with default values for missing parameters
 */
function loadStateFromURL() {
    const params = new URLSearchParams(window.location.search);

    const pageRaw = params.get('page') || '1';
    const page = /^[1-9]\d*$/.test(pageRaw) ? Number(pageRaw) : 1;

    const pageSizeRaw = params.get('pageSize') || '100';
    const pageSize = /^[1-9]\d*$/.test(pageSizeRaw) ? Number(pageSizeRaw) : 100;

    return {
        sortColumn: params.get('sort') || 'number',
        sortDirection: params.get('dir') || 'asc',
        search: params.get('q') || '',
        statusFilter: params.get('status') || '',
        prizeFilter: params.get('prize') || '',
        formalizedFilter: params.get('formalized') || '',
        oeisFilter: params.get('oeis') || '',
        selectedTags: params.get('tags') ? params.get('tags').split(',').filter(tag => tag.trim() !== '') : [],
        tagLogic: params.get('tagLogic') || 'any',
        tagSort: params.get('tagSort') || 'count',
        page,
        pageSize
    };
}

/**
 * Restore UI controls to match the given state
 * @param {Object} state - State object from loadStateFromURL()
 */
function restoreUIState(state) {
    // Restore search box
    const searchBox = document.getElementById('search-box');
    if (searchBox) {
        searchBox.value = state.search;
    }

    // Restore filter dropdowns
    const statusFilter = document.getElementById('filter-status');
    if (statusFilter) {
        statusFilter.value = state.statusFilter;
    }

    const prizeFilter = document.getElementById('filter-prize');
    if (prizeFilter) {
        prizeFilter.value = state.prizeFilter;
    }

    const formalizedFilter = document.getElementById('filter-formalized');
    if (formalizedFilter) {
        formalizedFilter.value = state.formalizedFilter;
    }

    const oeisFilter = document.getElementById('filter-oeis');
    if (oeisFilter) {
        oeisFilter.value = state.oeisFilter;
    }

    // Restore tag logic toggle
    if (state.tagLogic === 'all') {
        const tagLogicAll = document.getElementById('tag-logic-all');
        if (tagLogicAll) {
            tagLogicAll.checked = true;
        }
    } else {
        const tagLogicAny = document.getElementById('tag-logic-any');
        if (tagLogicAny) {
            tagLogicAny.checked = true;
        }
    }

    // Restore tag checkboxes (will be called after tags are populated)
    if (state.selectedTags && state.selectedTags.length > 0) {
        state.selectedTags.forEach(tag => {
            const checkbox = document.getElementById(`tag-${sanitizeTagId(tag)}`);
            if (checkbox) {
                checkbox.checked = true;
            }
        });
    }

    // Restore tag sort toggle
    if (state.tagSort === 'alpha') {
        const tagSortAlpha = document.getElementById('tag-sort-alpha');
        if (tagSortAlpha) {
            tagSortAlpha.checked = true;
        }
    } else {
        const tagSortCount = document.getElementById('tag-sort-count');
        if (tagSortCount) {
            tagSortCount.checked = true;
        }
    }

    // Restore sort indicators
    updateSortIndicators(state.sortColumn, state.sortDirection);
}

/**
 * Update visual sort indicators on table headers
 * @param {string} column - Column being sorted
 * @param {string} direction - Sort direction ('asc' or 'desc')
 */
function updateSortIndicators(column, direction) {
    // Remove all sort classes
    document.querySelectorAll('th.sortable').forEach(th => {
        th.classList.remove('sorted-asc', 'sorted-desc');
        const arrow = th.querySelector('.sort-arrow');
        if (arrow) {
            arrow.textContent = '';
        }
    });

    // Add sort class to active column
    const activeHeader = document.querySelector(`th[data-sort="${column}"]`);
    if (activeHeader) {
        activeHeader.classList.add(direction === 'asc' ? 'sorted-asc' : 'sorted-desc');
        const arrow = activeHeader.querySelector('.sort-arrow');
        if (arrow) {
            arrow.textContent = direction === 'asc' ? '▲' : '▼';
        }
    }
}

/**
 * Sanitize tag name for use as HTML ID
 * Replaces spaces and special characters with hyphens
 * @param {string} tag - Tag name
 * @returns {string} Sanitized tag ID
 */
function sanitizeTagId(tag) {
    return tag.replace(/[^a-zA-Z0-9]/g, '-').toLowerCase();
}

/**
 * Get current state from UI controls
 * @returns {Object} Current state object
 */
function getCurrentState() {
    const searchBox = document.getElementById('search-box');
    const statusFilter = document.getElementById('filter-status');
    const prizeFilter = document.getElementById('filter-prize');
    const formalizedFilter = document.getElementById('filter-formalized');
    const oeisFilter = document.getElementById('filter-oeis');

    // Get selected tags
    const selectedTags = [];
    document.querySelectorAll('.tag-checkbox-item input[type="checkbox"]:checked').forEach(checkbox => {
        selectedTags.push(checkbox.value);
    });

    // Get tag logic
    const tagLogicAll = document.getElementById('tag-logic-all');
    const tagLogic = tagLogicAll && tagLogicAll.checked ? 'all' : 'any';

    // Get tag sort preference
    const tagSortAlpha = document.getElementById('tag-sort-alpha');
    const tagSort = tagSortAlpha && tagSortAlpha.checked ? 'alpha' : 'count';

    // Get current sort state from table headers
    let sortColumn = 'number';
    let sortDirection = 'asc';
    const sortedHeader = document.querySelector('th.sorted-asc, th.sorted-desc');
    if (sortedHeader) {
        sortColumn = sortedHeader.getAttribute('data-sort');
        sortDirection = sortedHeader.classList.contains('sorted-asc') ? 'asc' : 'desc';
    }

    return {
        sortColumn,
        sortDirection,
        search: searchBox ? searchBox.value : '',
        statusFilter: statusFilter ? statusFilter.value : '',
        prizeFilter: prizeFilter ? prizeFilter.value : '',
        formalizedFilter: formalizedFilter ? formalizedFilter.value : '',
        oeisFilter: oeisFilter ? oeisFilter.value : '',
        selectedTags,
        tagLogic,
        tagSort,
        page: (typeof currentPage !== 'undefined' && Number.isFinite(currentPage)) ? currentPage : 1,
        pageSize: (typeof pageSize !== 'undefined' && Number.isFinite(pageSize)) ? pageSize : 100
    };
}
