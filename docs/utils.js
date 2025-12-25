/**
 * Utility functions for Erdos Problems Interactive Table
 * Handles link generation and data extraction
 */

/**
 * Render problem number as a link to erdosproblems.com
 * @param {string} number - Problem number
 * @returns {string} HTML anchor tag
 */
function renderProblemLink(number) {
    return `<a href="https://www.erdosproblems.com/${number}" target="_blank">${number}</a>`;
}

/**
 * Render OEIS codes as links or plain text
 * @param {Array<string>} oeisCodes - Array of OEIS codes
 * @returns {string} Comma-separated links/text
 */
function renderOEISLinks(oeisCodes) {
    if (!oeisCodes || oeisCodes.length === 0) {
        return '';
    }

    // OEIS code pattern: A followed by 6 digits
    const oeisPattern = /^A\d{6}$/;

    return oeisCodes.map(code => {
        if (oeisPattern.test(code)) {
            return `<a href="https://oeis.org/${code}" target="_blank">${code}</a>`;
        }
        // Non-linkable codes: N/A, possible, submitted, in progress, etc.
        return code;
    }).join(', ');
}

/**
 * Render formalized status with link to Lean file if available
 * @param {string} number - Problem number
 * @param {string} state - Formalized state (yes/no)
 * @returns {string} HTML link or plain text
 */
function renderFormalizedLink(number, state) {
    if (state === 'yes') {
        const leanURL = `https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/${number}.lean`;
        return `<a href="${leanURL}" target="_blank">yes</a>`;
    }
    return state || 'no';
}

/**
 * Extract column value from problem object
 * @param {Object} problem - Problem data object
 * @param {string} column - Column name
 * @returns {string|number} Column value
 */
function getColumnValue(problem, column) {
    switch (column) {
        case 'number':
            return problem.number || '';

        case 'prize':
            return problem.prize || 'no';

        case 'status':
            return (problem.status && problem.status.state) || '';

        case 'formalized':
            return (problem.formalized && problem.formalized.state) || 'no';

        case 'oeis':
            return (problem.oeis && problem.oeis.length > 0) ? problem.oeis.join(', ') : '';

        case 'tags':
            return (problem.tags && problem.tags.length > 0) ? problem.tags.join(', ') : '';

        case 'comments':
            return problem.comments || '';

        default:
            return '';
    }
}

/**
 * Parse prize value to numeric amount for sorting
 * @param {string} prize - Prize string (e.g., "$500", "no")
 * @returns {number} Numeric prize amount (0 for "no")
 */
function parsePrize(prize) {
    if (!prize || prize === 'no') {
        return 0;
    }
    // Extract numeric value from string like "$500"
    const match = prize.match(/\d+/);
    return match ? parseInt(match[0], 10) : 0;
}

/**
 * Escape HTML special characters to prevent XSS
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Render prize value with formatting
 * @param {string} prize - Prize string
 * @returns {string} Formatted prize display
 */
function renderPrize(prize) {
    if (!prize || prize === 'no') {
        return 'No';
    }
    return escapeHtml(prize);
}

/**
 * Render tags as comma-separated list
 * @param {Array<string>} tags - Array of tag strings
 * @returns {string} Formatted tag list
 */
function renderTags(tags) {
    if (!tags || tags.length === 0) {
        return '';
    }
    return tags.map(tag => escapeHtml(tag)).join(', ');
}

/**
 * Render status with formatting
 * @param {Object} status - Status object
 * @returns {string} Formatted status display
 */
function renderStatus(status) {
    if (!status || !status.state) {
        return '';
    }
    return escapeHtml(status.state);
}

/**
 * Render comments with escaping
 * @param {string} comments - Comments text
 * @returns {string} Escaped comments
 */
function renderComments(comments) {
    return escapeHtml(comments || '');
}

/**
 * Extract all unique tags with their counts from problems array
 * @param {Array<Object>} problems - Array of problem objects
 * @returns {Map<string, number>} Map of tag to count
 */
function extractTagCounts(problems) {
    const tagCounts = new Map();
    problems.forEach(problem => {
        if (problem.tags && Array.isArray(problem.tags)) {
            problem.tags.forEach(tag => {
                tagCounts.set(tag, (tagCounts.get(tag) || 0) + 1);
            });
        }
    });
    return tagCounts;
}

/**
 * Extract all unique tags from problems array, sorted by preference
 * @param {Array<Object>} problems - Array of problem objects
 * @param {string} sortBy - 'count' (default) or 'alpha'
 * @param {Map<string, number>} tagCounts - Optional pre-computed tag counts
 * @returns {Array<string>} Sorted array of unique tags
 */
function extractAllTags(problems, sortBy = 'count', tagCounts = null) {
    const counts = tagCounts || extractTagCounts(problems);
    const tags = Array.from(counts.keys());

    if (sortBy === 'alpha') {
        return tags.sort();
    } else {
        // Sort by count descending, then alphabetically for ties
        return tags.sort((a, b) => {
            const countDiff = counts.get(b) - counts.get(a);
            return countDiff !== 0 ? countDiff : a.localeCompare(b);
        });
    }
}

/**
 * Extract all unique status values from problems array
 * @param {Array<Object>} problems - Array of problem objects
 * @returns {Array<string>} Sorted array of unique statuses
 */
function extractAllStatuses(problems) {
    const statusSet = new Set();
    problems.forEach(problem => {
        if (problem.status && problem.status.state) {
            statusSet.add(problem.status.state);
        }
    });
    return Array.from(statusSet).sort();
}
