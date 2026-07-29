/**
 * Utility functions for Erdos Problems Interactive Table
 * Handles link generation and data extraction
 */

/**
 * Value of formal_status.state meaning "no formalized solution is known".
 * @type {string}
 */
const UNFORMALIZED = 'unformalized';

/**
 * Split a combined status such as "proved (Lean)" into its two primitives.
 * Mirrors split_legacy_status() in scripts/derive_status.py.
 * @param {string} state - Combined status state
 * @returns {{informal: string, formal: string}}
 */
function splitCombinedStatus(state) {
    const trimmed = (state || '').trim();
    const match = trimmed.match(/^(.*?)\s*\(([^()]+)\)$/);
    if (match) {
        return { informal: match[1].trim(), formal: match[2].trim() };
    }
    return { informal: trimmed, formal: UNFORMALIZED };
}

/**
 * Informal (human/mathematical) status of a problem.
 * Falls back to splitting the combined `status` for data that predates the
 * informal_status/formal_status split.
 * @param {Object} problem - Problem data object
 * @returns {string} Informal status state
 */
function getInformalState(problem) {
    const explicit = problem && problem.informal_status && problem.informal_status.state;
    if (explicit) return explicit;
    return splitCombinedStatus(problem && problem.status && problem.status.state).informal;
}

/**
 * Proof assistant in which a *solution* has been formalized, or "unformalized".
 * @param {Object} problem - Problem data object
 * @returns {string} Formal status state
 */
function getFormalState(problem) {
    const explicit = problem && problem.formal_status && problem.formal_status.state;
    if (explicit) return explicit;
    return splitCombinedStatus(problem && problem.status && problem.status.state).formal;
}

/**
 * Whether a solution to the problem has been formalized in some proof assistant
 * @param {Object} problem - Problem data object
 * @returns {boolean}
 */
function hasFormalizedSolution(problem) {
    const formal = getFormalState(problem);
    return Boolean(formal) && formal.toLowerCase() !== UNFORMALIZED;
}

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
 * Render statement-formalization status with a link to the Lean file if available
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
 * Informal statuses for which an AI attempt is still worth viewing
 * @type {Array<string>}
 */
const AI_ELIGIBLE_STATES = ['open', 'verifiable', 'independent', 'falsifiable'];

/**
 * Render AI Attempts link based on problem status
 * @param {string} number - Problem number
 * @param {Object} problem - Problem data object
 * @returns {string} HTML anchor tag with "view" or "add" text
 */
function renderAIAttempts(number, problem) {
    const url = `https://mehmetmars7.github.io/Erdosproblems-llm-hunter/problem.html?type=erdos&id=${number}`;
    // Keyed on the informal status, so that a formalized-but-undigested problem
    // ("open (Lean)") is still treated as open here.
    const state = getInformalState(problem).toLowerCase();
    const linkText = AI_ELIGIBLE_STATES.includes(state) ? 'view' : 'add';
    return `<a href="${url}" target="_blank" rel="noopener noreferrer">${linkText}</a>`;
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

        case 'formal':
            return getFormalState(problem);

        case 'oeis':
            return (problem.oeis && problem.oeis.length > 0) ? problem.oeis.join(', ') : '';

        case 'tags':
            return (problem.tags && problem.tags.length > 0) ? problem.tags.join(', ') : '';

        case 'comments':
            return problem.comments || '';
            
        case 'ai_attempts':
            return AI_ELIGIBLE_STATES.includes(getInformalState(problem).toLowerCase()) ? 'view' : 'add';
            
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
 * Escape text for use inside a double-quoted HTML attribute.
 * escapeHtml() is not sufficient there, as it leaves quotes untouched.
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeAttr(text) {
    if (!text) return '';
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
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
 * Render the combined status: the informal status, followed by the proof
 * assistant in which a solution has been formalized (if any).  The suffix is
 * tagged separately so it can be explained on hover and linked to the
 * formalization, since "(Lean)" here means the *solution* was formalized -
 * not the statement, which is what the "Statement formalized" column reports.
 * @param {Object} problem - Problem data object
 * @returns {string} Formatted status display
 */
function renderStatus(problem) {
    const informal = getInformalState(problem);
    if (!informal && !hasFormalizedSolution(problem)) {
        return '';
    }

    let html = escapeHtml(informal);
    if (hasFormalizedSolution(problem)) {
        const formal = getFormalState(problem);
        const label = `(${escapeHtml(formal)})`;
        const title = `A solution to this problem has been formalized in ${formal}`;
        const url = problem.formal_status && problem.formal_status.url;
        const suffix = /^https?:\/\//i.test(url || '')
            ? `<a class="formal-tag" href="${escapeAttr(url)}" target="_blank" rel="noopener noreferrer" title="${escapeAttr(title)}">${label}</a>`
            : `<span class="formal-tag" title="${escapeAttr(title)}">${label}</span>`;
        html += (html ? ' ' : '') + suffix;
    }
    return html;
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
 * Check if any non-tag filters are currently active
 * @returns {boolean} True if search or any dropdown filter is active
 */
function hasNonTagFilters() {
    const searchBox = document.getElementById('search-box');
    const searchQuery = searchBox ? searchBox.value.trim() : '';
    if (searchQuery !== '') return true;

    const statusFilter = document.getElementById('filter-status');
    if (statusFilter && statusFilter.value !== '') return true;

    const formalFilter = document.getElementById('filter-formal');
    if (formalFilter && formalFilter.value !== '') return true;

    const prizeFilter = document.getElementById('filter-prize');
    if (prizeFilter && prizeFilter.value !== '') return true;

    const formalizedFilter = document.getElementById('filter-formalized');
    if (formalizedFilter && formalizedFilter.value !== '') return true;

    const oeisFilter = document.getElementById('filter-oeis');
    if (oeisFilter && oeisFilter.value !== '') return true;

    return false;
}

/**
 * Extract and sort tags with two-tier logic (active tags first, then inactive)
 * @param {Array<Object>} problems - Array of problem objects
 * @param {string} sortBy - 'count' or 'alpha'
 * @param {Map<string, number>} totalCounts - Total tag counts
 * @param {Map<string, number>} filteredCounts - Filtered tag counts (or null)
 * @returns {Array<string>} Sorted array with active tags first, then inactive tags
 */
function extractAllTagsWithActivity(problems, sortBy, totalCounts, filteredCounts) {
    if (!filteredCounts) {
        // No filtered counts, use regular sorting
        return extractAllTags(problems, sortBy, totalCounts);
    }

    const allTags = Array.from(totalCounts.keys());
    const activeTags = [];
    const inactiveTags = [];

    // Separate tags into active and inactive
    allTags.forEach(tag => {
        const filteredCount = filteredCounts.get(tag) || 0;
        if (filteredCount > 0) {
            activeTags.push(tag);
        } else {
            inactiveTags.push(tag);
        }
    });

    // Sort each group
    if (sortBy === 'alpha') {
        activeTags.sort();
        inactiveTags.sort();
    } else {
        // Sort by filtered count for active tags
        activeTags.sort((a, b) => {
            const countDiff = filteredCounts.get(b) - filteredCounts.get(a);
            return countDiff !== 0 ? countDiff : a.localeCompare(b);
        });
        // Sort by total count for inactive tags
        inactiveTags.sort((a, b) => {
            const countDiff = totalCounts.get(b) - totalCounts.get(a);
            return countDiff !== 0 ? countDiff : a.localeCompare(b);
        });
    }

    return [...activeTags, ...inactiveTags];
}

/**
 * Extract informal status counts from problems array
 * @param {Array<Object>} problems - Array of problem objects
 * @returns {Map<string, number>} Map of informal status values to counts
 */
function extractStatusCounts(problems) {
    const statusCounts = new Map();
    problems.forEach(problem => {
        const status = getInformalState(problem) || 'open';
        statusCounts.set(status, (statusCounts.get(status) || 0) + 1);
    });
    return statusCounts;
}

/**
 * Extract formal (solution formalization) status counts from problems array
 * @param {Array<Object>} problems - Array of problem objects
 * @returns {Map<string, number>} Map of formal status values to counts
 */
function extractFormalStatusCounts(problems) {
    const counts = new Map();
    problems.forEach(problem => {
        const state = getFormalState(problem) || UNFORMALIZED;
        counts.set(state, (counts.get(state) || 0) + 1);
    });
    return counts;
}

/**
 * Extract prize counts from problems array
 * @param {Array<Object>} problems - Array of problem objects
 * @returns {Object} Object with yes/no counts
 */
function extractPrizeCounts(problems) {
    const counts = { yes: 0, no: 0 };
    problems.forEach(problem => {
        const hasPrize = problem.prize && problem.prize !== 'no';
        if (hasPrize) {
            counts.yes++;
        } else {
            counts.no++;
        }
    });
    return counts;
}

/**
 * Extract formalized counts from problems array
 * @param {Array<Object>} problems - Array of problem objects
 * @returns {Object} Object with yes/no counts
 */
function extractFormalizedCounts(problems) {
    const counts = { yes: 0, no: 0 };
    problems.forEach(problem => {
        const formalizedState = (problem.formalized && problem.formalized.state) || 'no';
        if (formalizedState === 'yes') {
            counts.yes++;
        } else {
            counts.no++;
        }
    });
    return counts;
}

/**
 * Extract OEIS counts from problems array
 * @param {Array<Object>} problems - Array of problem objects
 * @returns {Object} Object with linked/na/possible/submitted/inprogress counts
 */
function extractOEISCounts(problems) {
    const counts = { linked: 0, na: 0, possible: 0, submitted: 0, inprogress: 0 };
    problems.forEach(problem => {
        const oeis = problem.oeis || [];
        const oeisPattern = /^A\d{6}$/;

        if (oeis.some(code => oeisPattern.test(code))) {
            counts.linked++;
        }
        if (oeis.includes('N/A')) {
            counts.na++;
        }
        if (oeis.includes('possible')) {
            counts.possible++;
        }
        if (oeis.includes('submitted')) {
            counts.submitted++;
        }
        if (oeis.includes('in progress')) {
            counts.inprogress++;
        }
    });
    return counts;
}

/**
 * Extract all unique informal status values from problems array
 * @param {Array<Object>} problems - Array of problem objects
 * @returns {Array<string>} Sorted array of unique informal statuses
 */
function extractAllStatuses(problems) {
    const statusSet = new Set();
    problems.forEach(problem => {
        const state = getInformalState(problem);
        if (state) {
            statusSet.add(state);
        }
    });
    return Array.from(statusSet).sort();
}
