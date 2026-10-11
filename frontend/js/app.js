const API_URL = `${window.RESEARCHCOPILOT_API_URL || "http://127.0.0.1:8000"}/api/research`;
const form = document.getElementById("research-form");
const queryInput = document.getElementById("research-query");
const researchButton = document.getElementById("research-button");
const buttonText = document.getElementById("button-text");
const loading = document.getElementById("loading");
const loadingMessage = document.getElementById("loading-message");
const errorMessage = document.getElementById("error-message");
const resultsSection = document.getElementById("results-section");
const resultsQuery = document.getElementById("results-query");
const paperCount = document.getElementById("paper-count");

const panels = {
    papers: document.getElementById("panel-papers"),
    analyses: document.getElementById("panel-analyses"),
    summaries: document.getElementById("panel-summaries"),
    reviews: document.getElementById("panel-reviews"),
    report: document.getElementById("panel-report")
};

const resultLists = {
    papers: document.getElementById("papers-list"),
    analyses: document.getElementById("analyses-list"),
    summaries: document.getElementById("summaries-list"),
    reviews: document.getElementById("reviews-list"),
    report: document.getElementById("report-content")
};

// Safely display content as text, not executable HTML.
function createTextElement(tag, text, className = "") {
    const element = document.createElement(tag);
    element.textContent = text ?? "";

    if (className) {
        element.className = className;
    }

    return element;
}

function formatValue(value) {
    if (value === null || value === undefined || value === "") {
        return "Not reported";
    }

    if (Array.isArray(value)) {
        return value.length
            ? value.map(formatValue).join("; ")
            : "Not reported";
    }

    if (typeof value === "object") {
        return Object.entries(value)
            .map(([key, item]) => `${key}: ${formatValue(item)}`)
            .join("; ");
    }

    return String(value);
}

function createCard(title) {
    const card = document.createElement("article");
    card.className = "result-card";
    card.appendChild(createTextElement("h3", title || "Untitled"));
    return card;
}

function addField(card, label, value) {
    const section = document.createElement("div");
    section.className = "result-field";

    section.appendChild(createTextElement("h4", label));
    section.appendChild(createTextElement("p", formatValue(value)));

    card.appendChild(section);
}

function showEmptyState(container, message) {
    container.replaceChildren(
        createTextElement("p", message, "empty-state")
    );
}

function renderPapers(papers) {
    const container = resultLists.papers;
    container.replaceChildren();

    if (!papers.length) {
        showEmptyState(
            container,
            "No papers were found for this research question."
        );
        return;
    }

    papers.forEach((paper) => {
        const card = createCard(paper.title);

        const metadata = [
            paper.year,
            paper.venue,
            paper.citation_count !== null &&
            paper.citation_count !== undefined
                ? `${paper.citation_count} citations`
                : null
        ].filter(Boolean);

        if (metadata.length) {
            card.appendChild(
                createTextElement("p", metadata.join(" · "), "paper-meta")
            );
        }

        addField(card, "Abstract", paper.abstract);
        addField(card, "Authors", paper.authors);

        if (typeof paper.url === "string") {
            try {
                const url = new URL(paper.url);

                if (url.protocol === "https:" || url.protocol === "http:") {
                    const link = createTextElement("a", "View original paper");
                    link.href = url.href;
                    link.target = "_blank";
                    link.rel = "noopener noreferrer";
                    link.className = "paper-link";
                    card.appendChild(link);
                }
            } catch {
                // Ignore invalid paper URLs.
            }
        }

        container.appendChild(card);
    });
}

function renderAnalyses(analyses) {
    const container = resultLists.analyses;
    container.replaceChildren();

    if (!analyses.length) {
        showEmptyState(container, "No paper analyses are available.");
        return;
    }

    analyses.forEach((analysis) => {
        const card = createCard(analysis.title);

        const fields = [
            ["Research problem", analysis.research_problem],
            ["Research objective", analysis.research_objective],
            ["Methodology", analysis.methodology],
            ["Models and algorithms", analysis.models_and_algorithms],
            ["Datasets", analysis.datasets],
            ["Experimental setup", analysis.experimental_setup],
            ["Evaluation metrics", analysis.evaluation_metrics],
            ["Quantitative results", analysis.quantitative_results],
            ["Key findings", analysis.key_findings],
            ["Strengths", analysis.strengths],
            ["Limitations", analysis.limitations],
            ["Future work", analysis.future_work],
            ["Reported facts", analysis.reported_facts],
            ["Cautious inferences", analysis.cautious_inferences],
            ["Evidence", analysis.evidence],
            ["Source type", analysis.source_type],
            ["Unavailable information", analysis.unavailable_information]
        ];

        fields.forEach(([label, value]) => addField(card, label, value));
        container.appendChild(card);
    });
}

function renderSummaries(summaries) {
    const container = resultLists.summaries;
    container.replaceChildren();

    if (!summaries.length) {
        showEmptyState(container, "No summaries are available.");
        return;
    }

    summaries.forEach((summary) => {
        const card = createCard(summary.title);

        const fields = [
            ["Executive summary", summary.executive_summary],
            ["Research problem", summary.research_problem],
            ["Methodology", summary.methodology],
            ["Key contributions", summary.key_contributions],
            ["Key findings", summary.key_findings],
            ["Strengths", summary.strengths],
            ["Limitations", summary.limitations],
            ["Future work", summary.future_work]
        ];

        fields.forEach(([label, value]) => addField(card, label, value));
        container.appendChild(card);
    });
}

function renderReviews(reviews) {
    const container = resultLists.reviews;
    container.replaceChildren();

    if (!reviews.length) {
        showEmptyState(container, "No Critic reviews are available.");
        return;
    }

    reviews.forEach((review) => {
        const card = createCard(review.title);

        addField(card, "Overall assessment", review.overall_assessment);
        addField(card, "Review confidence", review.confidence);
        addField(card, "Evidence limitations", review.evidence_limitations);
        addField(card, "Strengths", review.strengths);
        addField(card, "Issues found", review.issues_found);
        addField(card, "Missing evidence", review.missing_evidence);
        addField(card, "Recommendations", review.recommendations);

        const claimReviews = Array.isArray(review.claim_reviews)
            ? review.claim_reviews
            : [];

        if (claimReviews.length) {
            card.appendChild(createTextElement("h4", "Claim-by-claim review"));

            claimReviews.forEach((claim, index) => {
                const claimSection = document.createElement("section");
                claimSection.className = "result-field";

                claimSection.appendChild(
                    createTextElement("h4", `Claim ${index + 1}`)
                );
                claimSection.appendChild(
                    createTextElement("p", formatValue(claim.claim))
                );
                claimSection.appendChild(
                    createTextElement(
                        "p",
                        `Verdict: ${formatValue(claim.verdict)}`
                    )
                );

                addField(
                    claimSection,
                    "Available evidence",
                    claim.evidence
                );
                addField(
                    claimSection,
                    "Explanation",
                    claim.explanation
                );
                addField(
                    claimSection,
                    "Suggested correction",
                    claim.suggested_correction
                );

                card.appendChild(claimSection);
            });
        } else {
            addField(card, "Claim reviews", "No individual claims were returned.");
        }

        container.appendChild(card);
    });
}

function renderReport(report) {
    const container = resultLists.report;
    container.replaceChildren();

    if (!report) {
        showEmptyState(container, "No final research report is available.");
        return;
    }

    const card = createCard(report.title);

    const fields = [
        ["Abstract", report.abstract],
        ["Introduction", report.introduction],
        ["Research objectives", report.research_objectives],
        ["Literature review", report.literature_review],
        ["Methodology comparison", report.methodology_comparison],
        ["Key findings", report.key_findings],
        ["Critical analysis", report.critical_analysis],
        ["Research gaps", report.research_gaps],
        ["Future directions", report.future_directions],
        ["Conclusion", report.conclusion],
        ["References", report.references],
        ["Limitations of this review", report.limitations_of_review]
    ];

    fields.forEach(([label, value]) => addField(card, label, value));
    container.appendChild(card);
}

function showTab(tabName) {
    Object.entries(panels).forEach(([name, panel]) => {
        if (panel) {
            panel.classList.toggle("hidden", name !== tabName);
        }
    });

    document.querySelectorAll("[data-tab]").forEach((tab) => {
        const isActive = tab.dataset.tab === tabName;
        tab.classList.toggle("active", isActive);
        tab.setAttribute("aria-selected", String(isActive));
    });
}

document.querySelectorAll("[data-tab]").forEach((tab) => {
    tab.addEventListener("click", () => showTab(tab.dataset.tab));
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const query = queryInput.value.trim();

    errorMessage.textContent = "";
    errorMessage.classList.add("hidden");

    if (!query) {
        errorMessage.textContent =
            "Please enter a research question or topic.";
        errorMessage.classList.remove("hidden");
        queryInput.focus();
        return;
    }

    researchButton.disabled = true;
    buttonText.textContent = "Researching...";
    loading.classList.remove("hidden");
    loadingMessage.textContent =
        "Searching, analyzing, summarizing, reviewing, and writing...";
    resultsSection.classList.add("hidden");

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query })
        });

        const data = await response.json();

        if (!response.ok) {
            const detail = typeof data.detail === "string"
                ? data.detail
                : "The research request failed.";

            throw new Error(detail);
        }

        const papers = data.papers ?? [];
        const analyses = data.analyses ?? [];
        const summaries = data.summaries ?? [];
        const reviews = data.reviews ?? [];

        renderPapers(papers);
        renderAnalyses(analyses);
        renderSummaries(summaries);
        renderReviews(reviews);
        renderReport(data.report);

        resultsQuery.textContent = `Research question: ${query}`;
        paperCount.textContent =
            `${data.total_found ?? papers.length} papers`;

        resultsSection.classList.remove("hidden");
        showTab("papers");

        resultsSection.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    } catch (error) {
        errorMessage.textContent =
            error instanceof TypeError
                ? "Cannot connect to ResearchCopilot. Please try again later."
                : error.message || "Something went wrong. Please try again.";

        errorMessage.classList.remove("hidden");
    } finally {
        researchButton.disabled = false;
        buttonText.textContent = "Start research";
        loading.classList.add("hidden");
    }
});