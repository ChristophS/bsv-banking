"use strict";

const state = {
  sort: "datum",
  direction: "desc",
  search: "",
  dateFrom: "",
  dateTo: "",
  hideCompletedVorgaengeTransactions: false,
  unclassifiedTransactionsOnly: false,
  linkCandidatesLoaded: false,
  linkCandidates: null,
  transactionRequest: null,
  vorgangRequest: null,
  overview: null,
  vorgaengeLoaded: false,
  vorgangTypesLoaded: false,
  vorgangTypes: [],
  vorgangSearch: "",
  vorgangHideCompleted: false,
  todosLoaded: false,
  todos: [],
  todoSearch: "",
  todoHideCompleted: false,
  todoVorgaenge: [],
  editingTodoId: null,
  termineLoaded: false,
  termine: [],
  terminSearch: "",
  terminHideCompleted: false,
  terminUnassignedUpcoming: false,
  terminVorgaenge: [],
  editingTerminId: null,
  budgetsLoaded: false,
  balanceHistory: null,
  selectedHistorySeries: new Set(["gesamt"]),
  rulesLoaded: false,
  ruleSearch: "",
  editingRuleId: null,
  ruleMatchFields: {},
  ruleMatchOperators: {},
  ruleLogicConnectors: {},
  completionRuleSearch: "",
  editingCompletionRuleId: null,
  completionRuleMatchFields: {},
  classificationOptions: {
    transaction_types: [],
    top_categories: [],
    sub_categories: [],
    sphere_defaults: [],
    spheres: [],
  },
  playerPremiumLoaded: false,
  playerPaymentLoaded: false,
  playerPaymentManualAvailable: false,
  playerPaymentResult: null,
  manualOffsetCounter: 0,
  editingPaymentPlayer: null,
  mailsLoaded: false,
  mails: [],
  mailLoadSequence: 0,
  mailSearch: "",
  selectedMailId: null,
  selectedMailDetail: null,
  selectedMailAttachment: null,
  entityPreviewAttachments: [],
  mailSpamThreshold: 0.7,
  mailZoom: 1,
  mailDeleteSelections: new Set(),
  mailSummaries: new Map(),
  mailSummaryOpen: new Set(),
  mailSummaryLoading: new Set(),
  mailVorgangReview: null,
  mailVorgangCandidates: [],
  mailVorgangSearch: "",
  mailVorgangHideCompleted: false,
  mailVorgangRequest: null,
};

const elements = {
  tabs: [...document.querySelectorAll("[data-tab]")],
  overviewCards: document.querySelector("#overview-cards"),
  dashboardRefresh: document.querySelector("#dashboard-refresh"),
  dashboardRefreshStatus: document.querySelector("#dashboard-refresh-status"),
  dashboardOpenVorgaenge: document.querySelector("#dashboard-open-vorgaenge"),
  dashboardOpenTodos: document.querySelector("#dashboard-open-todos"),
  dashboardUpcomingTermine: document.querySelector(
    "#dashboard-upcoming-termine",
  ),
  dashboardRouteButtons: [
    ...document.querySelectorAll("[data-dashboard-route]"),
  ],
  transactionPanel: document.querySelector("#transactions-panel"),
  vorgaengePanel: document.querySelector("#vorgaenge-panel"),
  terminePanel: document.querySelector("#termine-panel"),
  budgetPanel: document.querySelector("#budget-panel"),
  otherTasksPanel: document.querySelector("#other-tasks-panel"),
  search: document.querySelector("#transaction-search"),
  dateFrom: document.querySelector("#date-from"),
  dateTo: document.querySelector("#date-to"),
  transactionHideCompletedVorgaenge: document.querySelector(
    "#transaction-hide-completed-vorgaenge",
  ),
  resetPeriod: document.querySelector("#reset-period"),
  maxPeriod: document.querySelector("#max-period"),
  toggleBalanceHistory: document.querySelector("#toggle-balance-history"),
  balanceHistoryPanel: document.querySelector("#balance-history-panel"),
  historyDateFrom: document.querySelector("#history-date-from"),
  historyDateTo: document.querySelector("#history-date-to"),
  loadBalanceHistory: document.querySelector("#load-balance-history"),
  historySeriesSelector: document.querySelector("#history-series-selector"),
  balanceHistoryChart: document.querySelector("#balance-history-chart"),
  historyLoading: document.querySelector("#history-loading"),
  historyEmpty: document.querySelector("#history-empty"),
  toggleRules: document.querySelector("#toggle-rules"),
  rulesPanel: document.querySelector("#rules-panel"),
  ruleList: document.querySelector("#rule-list"),
  ruleCount: document.querySelector("#rule-count"),
  ruleSearch: document.querySelector("#rule-search"),
  ruleForm: document.querySelector("#rule-form"),
  ruleFormTitle: document.querySelector("#rule-form-title"),
  ruleSubmit: document.querySelector("#rule-submit"),
  ruleCancelEdit: document.querySelector("#rule-cancel-edit"),
  ruleFormStatus: document.querySelector("#rule-form-status"),
  ruleConditions: document.querySelector("#rule-conditions"),
  ruleAddCondition: document.querySelector("#rule-add-condition"),
  completionRuleList: document.querySelector("#completion-rule-list"),
  completionRuleCount: document.querySelector("#completion-rule-count"),
  completionRuleSearch: document.querySelector("#completion-rule-search"),
  completionRuleForm: document.querySelector("#completion-rule-form"),
  completionRuleFormTitle: document.querySelector(
    "#completion-rule-form-title",
  ),
  completionRuleSubmit: document.querySelector("#completion-rule-submit"),
  completionRuleCancelEdit: document.querySelector(
    "#completion-rule-cancel-edit",
  ),
  completionRuleFormStatus: document.querySelector(
    "#completion-rule-form-status",
  ),
  completionRuleConditions: document.querySelector(
    "#completion-rule-conditions",
  ),
  completionRuleAddCondition: document.querySelector(
    "#completion-rule-add-condition",
  ),
  refreshTransactions: document.querySelector("#refresh-transactions"),
  refreshStatus: document.querySelector("#refresh-status"),
  transactionRows: document.querySelector("#transaction-rows"),
  transactionTable: document.querySelector("#transaction-table"),
  transactionLoading: document.querySelector("#transaction-loading"),
  transactionEmpty: document.querySelector("#transaction-empty"),
  transactionCount: document.querySelector("#transaction-count"),
  transactionCountLabel: document.querySelector("#transaction-count-label"),
  totalBalance: document.querySelector("#total-balance"),
  totalBalanceLabel: document.querySelector("#total-balance-label"),
  totalBalanceNote: document.querySelector("#total-balance-note"),
  accountBalances: document.querySelector("#account-balances"),
  balanceCorrectionCount: document.querySelector("#balance-correction-count"),
  balanceCorrectionLoading: document.querySelector("#balance-correction-loading"),
  balanceCorrectionEmpty: document.querySelector("#balance-correction-empty"),
  balanceCorrectionList: document.querySelector("#balance-correction-list"),
  balanceCorrectionForm: document.querySelector("#balance-correction-form"),
  balanceCorrectionStatus: document.querySelector("#balance-correction-status"),
  sortButtons: [...document.querySelectorAll("[data-sort]")],
  vorgangSearch: document.querySelector("#vorgang-search"),
  vorgangHideCompleted: document.querySelector("#vorgang-hide-completed"),
  vorgangRows: document.querySelector("#vorgang-rows"),
  vorgangTable: document.querySelector("#vorgang-table"),
  vorgangLoading: document.querySelector("#vorgang-loading"),
  vorgangEmpty: document.querySelector("#vorgang-empty"),
  vorgangCount: document.querySelector("#vorgang-count"),
  vorgangCountLabel: document.querySelector("#vorgang-count-label"),
  vorgangCreate: document.querySelector("#vorgang-create"),
  todoPanel: document.querySelector("#todo-panel"),
  todoSearch: document.querySelector("#todo-search"),
  todoHideCompleted: document.querySelector("#todo-hide-completed"),
  todoCount: document.querySelector("#todo-count"),
  todoCountLabel: document.querySelector("#todo-count-label"),
  todoForm: document.querySelector("#todo-form"),
  todoFormTitle: document.querySelector("#todo-form-title"),
  todoTitle: document.querySelector("#todo-title"),
  todoDescription: document.querySelector("#todo-description"),
  todoDueDate: document.querySelector("#todo-due-date"),
  todoPriority: document.querySelector("#todo-priority"),
  todoVorgaenge: document.querySelector("#todo-vorgaenge"),
  todoSubmit: document.querySelector("#todo-submit"),
  todoCreateVorgang: document.querySelector("#todo-create-vorgang"),
  todoCancelEdit: document.querySelector("#todo-cancel-edit"),
  todoFormStatus: document.querySelector("#todo-form-status"),
  todoLoading: document.querySelector("#todo-loading"),
  todoList: document.querySelector("#todo-list"),
  todoEmpty: document.querySelector("#todo-empty"),
  terminSearch: document.querySelector("#termin-search"),
  terminHideCompleted: document.querySelector("#termin-hide-completed"),
  terminSpecialFilter: document.querySelector("#termin-special-filter"),
  terminSpecialFilterReset: document.querySelector(
    "#termin-special-filter-reset",
  ),
  terminCount: document.querySelector("#termin-count"),
  terminCountLabel: document.querySelector("#termin-count-label"),
  terminForm: document.querySelector("#termin-form"),
  terminFormTitle: document.querySelector("#termin-form-title"),
  terminTitle: document.querySelector("#termin-title"),
  terminDescription: document.querySelector("#termin-description"),
  terminStartsAt: document.querySelector("#termin-starts-at"),
  terminEndsAt: document.querySelector("#termin-ends-at"),
  terminLocation: document.querySelector("#termin-location"),
  terminStatus: document.querySelector("#termin-status"),
  terminVorgaenge: document.querySelector("#termin-vorgaenge"),
  terminSubmit: document.querySelector("#termin-submit"),
  terminCancelEdit: document.querySelector("#termin-cancel-edit"),
  terminFormStatus: document.querySelector("#termin-form-status"),
  terminLoading: document.querySelector("#termin-loading"),
  terminList: document.querySelector("#termin-list"),
  terminEmpty: document.querySelector("#termin-empty"),
  budgetRows: document.querySelector("#budget-rows"),
  budgetTable: document.querySelector("#budget-table"),
  budgetLoading: document.querySelector("#budget-loading"),
  budgetEmpty: document.querySelector("#budget-empty"),
  budgetCount: document.querySelector("#budget-count"),
  mailPanel: document.querySelector("#mail-panel"),
  mailSearch: document.querySelector("#mail-search"),
  mailSpamThreshold: document.querySelector("#mail-spam-threshold"),
  mailDeleteSpam: document.querySelector("#mail-delete-spam"),
  mailDeleteSelected: document.querySelector("#mail-delete-selected"),
  mailDeleteStatus: document.querySelector("#mail-delete-status"),
  mailRefresh: document.querySelector("#mail-refresh"),
  mailLoading: document.querySelector("#mail-loading"),
  mailList: document.querySelector("#mail-list"),
  mailEmpty: document.querySelector("#mail-empty"),
  mailCount: document.querySelector("#mail-count"),
  mailDetail: document.querySelector("#mail-detail"),
  playerPremiumForm: document.querySelector("#player-premium-form"),
  playerPremiumSeason: document.querySelector("#player-premium-season"),
  playerPremiumTeams: document.querySelector("#player-premium-teams"),
  playerPremiumSubmit: document.querySelector("#player-premium-submit"),
  playerPremiumStatus: document.querySelector("#player-premium-status"),
  playerPremiumLoading: document.querySelector("#player-premium-loading"),
  playerPremiumResults: document.querySelector("#player-premium-results"),
  playerPremiumResultMeta: document.querySelector(
    "#player-premium-result-meta",
  ),
  playerPremiumTables: document.querySelector("#player-premium-tables"),
  playerPaymentSubmit: document.querySelector("#player-payment-submit"),
  playerPaymentStatus: document.querySelector("#player-payment-status"),
  playerPaymentLoading: document.querySelector("#player-payment-loading"),
  playerPaymentResults: document.querySelector("#player-payment-results"),
  playerPaymentSummary: document.querySelector("#player-payment-summary"),
  playerPaymentTeams: document.querySelector("#player-payment-teams"),
  playerOffsetPanel: document.querySelector("#player-offset-panel"),
  playerOffsetDeckelPath: document.querySelector("#player-offset-deckel-path"),
  playerOffsetApply: document.querySelector("#player-offset-apply"),
  playerOffsetAddManual: document.querySelector("#player-offset-add-manual"),
  playerPaymentExport: document.querySelector("#player-payment-export"),
  playerOffsetStatus: document.querySelector("#player-offset-status"),
  playerOffsetReview: document.querySelector("#player-offset-review"),
  playerOffsetManualList: document.querySelector("#player-offset-manual-list"),
  playerPaymentDialog: document.querySelector("#player-payment-dialog"),
  playerPaymentForm: document.querySelector("#player-payment-form"),
  playerPaymentDialogTitle: document.querySelector(
    "#player-payment-dialog-title",
  ),
  playerPaymentDialogClose: document.querySelector(
    "#player-payment-dialog-close",
  ),
  playerPaymentDialogCancel: document.querySelector(
    "#player-payment-dialog-cancel",
  ),
  playerPaymentAccountHolder: document.querySelector(
    "#player-payment-account-holder",
  ),
  playerPaymentIban: document.querySelector("#player-payment-iban"),
  playerPaymentBic: document.querySelector("#player-payment-bic"),
  playerPaymentFormStatus: document.querySelector(
    "#player-payment-form-status",
  ),
  dialog: document.querySelector("#transaction-dialog"),
  detailEyebrow: document.querySelector("#detail-eyebrow"),
  detailTitle: document.querySelector("#detail-title"),
  detailSubtitle: document.querySelector("#detail-subtitle"),
  detailDialogStatus: document.querySelector("#detail-dialog-status"),
  detailContent: document.querySelector("#detail-content"),
  detailClose: document.querySelector("#detail-close"),
  entityDialog: document.querySelector("#entity-preview-dialog"),
  entityPreviewEyebrow: document.querySelector("#entity-preview-eyebrow"),
  entityPreviewTitle: document.querySelector("#entity-preview-title"),
  entityPreviewSubtitle: document.querySelector("#entity-preview-subtitle"),
  entityPreviewContent: document.querySelector("#entity-preview-content"),
  entityPreviewClose: document.querySelector("#entity-preview-close"),
  errorToast: document.querySelector("#error-toast"),
};

const currencyFormatter = new Intl.NumberFormat("de-DE", {
  style: "currency",
  currency: "EUR",
});

const integerFormatter = new Intl.NumberFormat("de-DE");

let searchTimer;
let vorgangSearchTimer;
let todoSearchTimer;
let terminSearchTimer;
let ruleSearchTimer;
let completionRuleSearchTimer;
let mailVorgangSearchTimer;
let toastTimer;
let refreshTimer;
let playerPremiumTimer;
let playerPaymentTimer;
let ruleDatalistCounter = 0;

const chartColors = [
  "#1c5943",
  "#2b77b8",
  "#a55a23",
  "#7a4da3",
  "#b13f64",
  "#56822f",
  "#756335",
];
const maxRuleConditions = 50;

elements.tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    if (tab.dataset.tab === "termine") {
      setTerminUnassignedUpcoming(false);
      state.termineLoaded = false;
    }
    if (tab.dataset.tab === "transactions") {
      state.unclassifiedTransactionsOnly = false;
      loadTransactions();
    }
    activateTab(tab.dataset.tab);
  });
});

elements.overviewCards.addEventListener("click", (event) => {
  const button = event.target.closest("[data-overview-entity]");
  if (!button) {
    return;
  }
  navigateFromOverviewCard(
    button.dataset.overviewKey,
    button.dataset.overviewEntity,
  );
});
elements.dashboardRouteButtons.forEach((button) => {
  button.addEventListener("click", () => {
    navigateFromOverviewCard("", button.dataset.dashboardRoute);
  });
});
[
  elements.dashboardOpenVorgaenge,
  elements.dashboardOpenTodos,
  elements.dashboardUpcomingTermine,
].forEach((container) => {
  container.addEventListener("click", (event) => {
    const button = event.target.closest("[data-overview-entity]");
    if (!button) {
      return;
    }
    navigateFromOverviewCard("", button.dataset.overviewEntity);
  });
});

elements.sortButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const requestedSort = button.dataset.sort;
    if (state.sort === requestedSort) {
      state.direction = state.direction === "asc" ? "desc" : "asc";
    } else {
      state.sort = requestedSort;
      state.direction = requestedSort === "datum" ? "desc" : "asc";
    }
    updateSortIndicators();
    loadTransactions();
  });
});

elements.search.addEventListener("input", () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    state.search = elements.search.value;
    loadTransactions();
  }, 220);
});

elements.transactionHideCompletedVorgaenge.addEventListener("change", () => {
  state.hideCompletedVorgaengeTransactions =
    elements.transactionHideCompletedVorgaenge.checked;
  loadTransactions();
});

elements.vorgangSearch.addEventListener("input", () => {
  clearTimeout(vorgangSearchTimer);
  vorgangSearchTimer = setTimeout(() => {
    state.vorgangSearch = elements.vorgangSearch.value;
    loadVorgaenge();
  }, 220);
});

elements.vorgangHideCompleted.addEventListener("change", () => {
  state.vorgangHideCompleted = elements.vorgangHideCompleted.checked;
  loadVorgaenge();
});
elements.vorgangCreate.addEventListener("click", () => {
  openVorgangCreateDialog();
});

elements.todoSearch.addEventListener("input", () => {
  clearTimeout(todoSearchTimer);
  todoSearchTimer = setTimeout(() => {
    state.todoSearch = elements.todoSearch.value;
    loadTodos();
  }, 220);
});
elements.todoHideCompleted.addEventListener("change", () => {
  state.todoHideCompleted = elements.todoHideCompleted.checked;
  loadTodos();
});
elements.todoForm.addEventListener("submit", saveTodo);
elements.todoCreateVorgang.addEventListener("click", saveTodoAndCreateVorgang);
elements.todoCancelEdit.addEventListener("click", resetTodoForm);
elements.todoList.addEventListener("click", handleTodoListClick);
elements.todoList.addEventListener("change", handleTodoListChange);
elements.terminSearch.addEventListener("input", () => {
  clearTimeout(terminSearchTimer);
  terminSearchTimer = setTimeout(() => {
    state.terminSearch = elements.terminSearch.value;
    loadTermine();
  }, 220);
});
elements.terminHideCompleted.addEventListener("change", () => {
  state.terminHideCompleted = elements.terminHideCompleted.checked;
  setTerminUnassignedUpcoming(false);
  loadTermine();
});
elements.terminSpecialFilterReset.addEventListener("click", () => {
  setTerminUnassignedUpcoming(false);
  state.termineLoaded = false;
  loadTermine();
});
elements.terminForm.addEventListener("submit", saveTermin);
elements.terminCancelEdit.addEventListener("click", resetTerminForm);
elements.terminList.addEventListener("click", handleTerminListClick);

elements.dateFrom.addEventListener("change", applyDateFilter);
elements.dateTo.addEventListener("change", applyDateFilter);
elements.resetPeriod.addEventListener("click", () => {
  setDefaultPeriod();
  loadTransactions();
});
elements.maxPeriod.addEventListener("click", setMaximumPeriod);

elements.toggleBalanceHistory.addEventListener("click", () => {
  const opening = elements.balanceHistoryPanel.hidden;
  elements.balanceHistoryPanel.hidden = !opening;
  elements.toggleBalanceHistory.textContent = opening
    ? "Kontoverlauf ausblenden"
    : "Kontoverlauf anzeigen";
  if (opening && !state.balanceHistory) {
    loadBalanceHistory();
  }
});

elements.loadBalanceHistory.addEventListener("click", loadBalanceHistory);

elements.toggleRules.addEventListener("click", () => {
  const opening = elements.rulesPanel.hidden;
  elements.rulesPanel.hidden = !opening;
  elements.toggleRules.textContent = opening
    ? "Regeln ausblenden"
    : "Regeln verwalten";
  if (opening && !state.rulesLoaded) {
    loadRules();
  }
});

elements.ruleForm.addEventListener("submit", createRule);
elements.ruleCancelEdit.addEventListener("click", resetRuleForm);
elements.ruleAddCondition.addEventListener("click", () => {
  addRuleCondition();
});
elements.ruleSearch.addEventListener("input", () => {
  clearTimeout(ruleSearchTimer);
  ruleSearchTimer = setTimeout(() => {
    state.ruleSearch = elements.ruleSearch.value;
    loadRules();
  }, 220);
});
elements.completionRuleForm.addEventListener(
  "submit",
  createCompletionRule,
);
elements.completionRuleCancelEdit.addEventListener(
  "click",
  resetCompletionRuleForm,
);
elements.completionRuleAddCondition.addEventListener("click", () => {
  addRuleCondition(
    {},
    elements.completionRuleConditions,
    elements.completionRuleAddCondition,
    state.completionRuleMatchFields,
  );
});
elements.completionRuleSearch.addEventListener("input", () => {
  clearTimeout(completionRuleSearchTimer);
  completionRuleSearchTimer = setTimeout(() => {
    state.completionRuleSearch = elements.completionRuleSearch.value;
    loadRules();
  }, 220);
});
elements.dashboardRefresh.addEventListener("click", requestRefresh);
elements.refreshTransactions.addEventListener("click", requestRefresh);
elements.mailRefresh.addEventListener("click", () => loadMails(true));
elements.mailDeleteSpam.addEventListener("click", deleteSpamMails);
elements.mailDeleteSelected.addEventListener("click", deleteSelectedMails);
elements.mailSearch.addEventListener("input", () => {
  state.mailSearch = elements.mailSearch.value;
  renderMailList();
});
elements.mailSpamThreshold.addEventListener(
  "change",
  updateMailSpamThreshold,
);
elements.mailList.addEventListener("click", handleMailListClick);
elements.mailList.addEventListener("change", handleMailSelectionChange);
elements.mailDetail.addEventListener("click", handleMailDetailClick);
elements.mailDetail.addEventListener("input", handleMailDetailInput);
elements.mailDetail.addEventListener("submit", handleMailDetailSubmit);
elements.entityPreviewContent.addEventListener("click", handleMailPreviewClick);
elements.entityPreviewContent.addEventListener("input", handleMailDetailInput);
elements.playerPremiumForm.addEventListener(
  "submit",
  requestPlayerPremiums,
);
elements.playerPaymentSubmit.addEventListener(
  "click",
  requestPlayerPayments,
);
elements.playerOffsetApply.addEventListener(
  "click",
  applyPlayerPaymentOffsets,
);
elements.playerOffsetAddManual.addEventListener(
  "click",
  () => addManualOffsetRow(),
);
elements.playerPaymentExport.addEventListener(
  "click",
  exportPlayerPaymentFiles,
);
elements.playerOffsetReview.addEventListener(
  "change",
  markPlayerOffsetsPending,
);
elements.playerOffsetManualList.addEventListener(
  "input",
  markPlayerOffsetsPending,
);
elements.playerOffsetManualList.addEventListener(
  "change",
  markPlayerOffsetsPending,
);
elements.playerPaymentForm.addEventListener(
  "submit",
  saveManualPlayerPayment,
);
elements.playerPaymentDialogClose.addEventListener(
  "click",
  closePlayerPaymentDialog,
);
elements.playerPaymentDialogCancel.addEventListener(
  "click",
  closePlayerPaymentDialog,
);

document.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
    event.preventDefault();
    elements.search.focus();
  }
});

elements.detailClose.addEventListener("click", () => {
  elements.dialog.close();
});

elements.entityPreviewClose.addEventListener("click", () => {
  elements.entityDialog.close();
});
elements.balanceCorrectionForm.addEventListener("submit", saveBalanceCorrection);

elements.dialog.addEventListener("click", (event) => {
  if (event.target === elements.dialog) {
    elements.dialog.close();
  }
});

elements.entityDialog.addEventListener("click", (event) => {
  if (event.target === elements.entityDialog) {
    elements.entityDialog.close();
  }
});

function activateTab(name) {
  const isTransactions = name === "transactions";
  const isVorgaenge = name === "vorgaenge";
  const isTodos = name === "todos";
  const isTermine = name === "termine";
  const isBudget = name === "budget";
  const isMail = name === "mail";
  const isOtherTasks = name === "other-tasks";
  elements.transactionPanel.hidden = !isTransactions;
  elements.vorgaengePanel.hidden = !isVorgaenge;
  elements.todoPanel.hidden = !isTodos;
  elements.terminePanel.hidden = !isTermine;
  elements.budgetPanel.hidden = !isBudget;
  elements.mailPanel.hidden = !isMail;
  elements.otherTasksPanel.hidden = !isOtherTasks;
  elements.tabs.forEach((tab) => {
    const active = tab.dataset.tab === name;
    tab.classList.toggle("is-active", active);
    tab.setAttribute("aria-selected", String(active));
  });
  if (isVorgaenge && !state.vorgaengeLoaded) {
    loadVorgaenge();
  }
  if (isTodos && !state.todosLoaded) {
    loadTodos();
  }
  if (isTermine && !state.termineLoaded) {
    loadTermine();
  }
  if (isBudget && !state.budgetsLoaded) {
    loadBudgets();
  }
  if (isMail && !state.mailsLoaded) {
    loadMails();
  }
  if (isOtherTasks && !state.playerPremiumLoaded) {
    loadPlayerPremiumStatus();
  }
  if (isOtherTasks && !state.playerPaymentLoaded) {
    loadPlayerPaymentStatus();
  }
}

async function loadOverview() {
  try {
    const response = await fetch("/api/overview");
    state.overview = await readResponse(response);
    renderOverview();
  } catch (error) {
    showError(error.message);
  }
}

function renderOverview() {
  elements.overviewCards.replaceChildren();
  const cards = state.overview?.cards || [];
  for (const card of cards) {
    const button = mailElement("button", "overview-card");
    button.type = "button";
    button.dataset.overviewKey = card.key || "";
    button.dataset.overviewEntity = card.entity || "vorgaenge";
    const isOpen = card.state === "open" && Number(card.count || 0) > 0;
    button.classList.toggle("is-empty", !isOpen);
    button.setAttribute(
      "aria-label",
      `Priorität ${card.priority}: ${card.label}, ${card.state_label}`,
    );
    button.append(
      mailElement(
        "span",
        "overview-card-priority",
        `${card.priority}. ${card.priority_label}`,
      ),
      mailElement("strong", "overview-card-label", card.label),
      mailElement("span", "overview-card-reason", card.reason || ""),
      mailElement("span", "overview-card-state", card.state_label),
    );
    elements.overviewCards.append(button);
  }
  renderDashboardPreviews();
}

function renderDashboardPreviews() {
  const previews = state.overview?.previews || {};
  renderDashboardPreviewList(
    elements.dashboardOpenVorgaenge,
    previews.open_vorgaenge || [],
    "vorgaenge",
    (item) => ({
      title: item.titel || item.bezug || "Vorgang ohne Titel",
      meta: [
        item.vorgangstyp,
        formatStatus(item.status),
        item.letztes_datum ? formatDate(item.letztes_datum) : "",
      ],
    }),
  );
  renderDashboardPreviewList(
    elements.dashboardOpenTodos,
    previews.open_todos || [],
    "todos",
    (item) => ({
      title: item.title || "To-Do ohne Titel",
      meta: [
        todoPriorityLabel(item.priority),
        item.due_date ? `Fällig: ${formatDate(item.due_date)}` : "",
      ],
    }),
  );
  renderDashboardPreviewList(
    elements.dashboardUpcomingTermine,
    previews.upcoming_termine || [],
    "termine",
    (item) => ({
      title: item.title || "Termin ohne Titel",
      meta: [
        item.starts_at ? formatDateTimeOrDate(item.starts_at) : "",
        item.location,
        terminStatusLabel(item.status),
      ],
    }),
  );
}

function renderDashboardPreviewList(target, items, entity, mapItem) {
  target.replaceChildren();
  if (!items.length) {
    target.append(
      mailElement("p", "dashboard-preview-empty", "Keine offenen Einträge."),
    );
    return;
  }
  for (const item of items) {
    const data = mapItem(item);
    const button = mailElement("button", "dashboard-preview-item");
    button.type = "button";
    button.dataset.overviewEntity = entity;
    button.append(
      mailElement("strong", "", data.title),
      mailElement(
        "span",
        "",
        data.meta.filter(Boolean).join(" · "),
      ),
    );
    target.append(button);
  }
}

const overviewCardRoutes = {
  byKey: {
    unclassified_transactions: () => {
      state.unclassifiedTransactionsOnly = true;
      activateTab("transactions");
      loadTransactions();
    },
    open_vorgaenge: () => {
      setVorgangHideCompleted(true);
      state.vorgaengeLoaded = false;
      activateTab("vorgaenge");
    },
    open_todos: () => {
      setTodoHideCompleted(true);
      state.todosLoaded = false;
      activateTab("todos");
    },
    unassigned_transactions: () => {
      state.unclassifiedTransactionsOnly = false;
      setTransactionHideCompletedVorgaenge(true);
      activateTab("transactions");
      loadTransactions();
    },
    // Termine share one entity, so key routes keep the current card-specific filters.
    upcoming_termine: () => {
      setTerminHideCompleted(true);
      setTerminUnassignedUpcoming(false);
      state.termineLoaded = false;
      activateTab("termine");
    },
    unassigned_termine: () => {
      setTerminHideCompleted(true);
      setTerminUnassignedUpcoming(true);
      state.termineLoaded = false;
      activateTab("termine");
    },
    unassigned_documents: openFirstUnassignedDocument,
  },
  byEntity: {
    documents: () => {
      state.vorgaengeLoaded = false;
      activateTab("vorgaenge");
    },
    mails: () => {
      state.mailsLoaded = false;
      activateTab("mail");
    },
    termine: () => {
      setTerminUnassignedUpcoming(false);
      state.termineLoaded = false;
      activateTab("termine");
    },
    todos: () => {
      state.todosLoaded = false;
      activateTab("todos");
    },
    transactions: () => {
      state.unclassifiedTransactionsOnly = false;
      activateTab("transactions");
      loadTransactions();
    },
    vorgaenge: () => {
      state.vorgaengeLoaded = false;
      activateTab("vorgaenge");
    },
  },
  fallback: () => {
    state.vorgaengeLoaded = false;
    activateTab("vorgaenge");
  },
};

async function openFirstUnassignedDocument() {
  try {
    const response = await fetch("/api/belege?unassigned_only=true");
    const payload = await readResponse(response);
    const beleg = payload.belege?.[0];
    if (!beleg) {
      await loadOverview();
      return;
    }
    await openVorgangCreateDialog({
      type: "beleg",
      id: beleg.beleg_id,
      title: beleg.dateiname || beleg.beleg_id,
      description: "Nicht zugewiesenes Dokument einem Vorgang zuordnen.",
    });
  } catch (error) {
    showError(error.message);
  }
}

function navigateFromOverviewCard(key, entity) {
  const route =
    ownOverviewRoute(overviewCardRoutes.byKey, key) ||
    ownOverviewRoute(overviewCardRoutes.byEntity, entity) ||
    overviewCardRoutes.fallback;
  route();
}

function ownOverviewRoute(routes, name) {
  if (Object.hasOwn(routes, name)) {
    return routes[name];
  }
  return null;
}

function setTransactionHideCompletedVorgaenge(value) {
  state.hideCompletedVorgaengeTransactions = value;
  elements.transactionHideCompletedVorgaenge.checked = value;
}

function setVorgangHideCompleted(value) {
  state.vorgangHideCompleted = value;
  elements.vorgangHideCompleted.checked = value;
}

function setTodoHideCompleted(value) {
  state.todoHideCompleted = value;
  elements.todoHideCompleted.checked = value;
}

function setTerminHideCompleted(value) {
  state.terminHideCompleted = value;
  elements.terminHideCompleted.checked = value;
}

function setTerminUnassignedUpcoming(value) {
  state.terminUnassignedUpcoming = value;
  renderTerminSpecialFilter();
}

function renderTerminSpecialFilter() {
  elements.terminSpecialFilter.hidden = !state.terminUnassignedUpcoming;
}

async function loadTodos() {
  elements.todoLoading.hidden = false;
  elements.todoEmpty.hidden = true;
  const parameters = new URLSearchParams({
    search: state.todoSearch,
    hide_completed: String(state.todoHideCompleted),
  });
  try {
    const requests = [
      fetch(`/api/todos?${parameters}`),
    ];
    if (!state.todoVorgaenge.length) {
      requests.push(fetch("/api/vorgaenge"));
    }
    const responses = await Promise.all(requests);
    const payload = await readResponse(responses[0]);
    if (responses[1]) {
      const vorgangPayload = await readResponse(responses[1]);
      state.todoVorgaenge = vorgangPayload.vorgaenge || [];
      renderTodoVorgangOptions(
        state.editingTodoId
          ? state.todos.find(
            (todo) => todo.todo_id === state.editingTodoId,
          )?.vorgangs_ids || []
          : [],
      );
    }
    state.todos = payload.todos || [];
    state.todosLoaded = true;
    elements.todoCount.textContent = integerFormatter.format(payload.count);
    elements.todoCountLabel.textContent =
      payload.count === 1 ? "To-Do" : "To-Dos";
    renderTodoList();
  } catch (error) {
    state.todos = [];
    renderTodoList();
    showError(error.message);
  } finally {
    elements.todoLoading.hidden = true;
  }
}

function renderTodoList() {
  elements.todoList.replaceChildren();
  elements.todoEmpty.hidden = state.todos.length > 0;
  for (const todo of state.todos) {
    const card = mailElement(
      "article",
      `todo-card ${todo.completed ? "is-completed" : ""}`,
    );
    card.dataset.todoId = todo.todo_id;

    const completionLabel = mailElement("label", "todo-completion");
    const completion = document.createElement("input");
    completion.type = "checkbox";
    completion.checked = Boolean(todo.completed);
    completion.dataset.toggleTodo = todo.todo_id;
    completion.setAttribute(
      "aria-label",
      todo.completed
        ? `${todo.title} wieder öffnen`
        : `${todo.title} abschließen`,
    );
    completionLabel.append(
      completion,
      mailElement(
        "span",
        "",
        todo.completed ? "Abgeschlossen" : "Offen",
      ),
    );

    const heading = mailElement("div", "todo-card-heading");
    const titleArea = mailElement("div");
    titleArea.append(
      mailElement("h3", "", todo.title),
      mailElement("code", "todo-id", todo.todo_id),
    );
    const badges = mailElement("div", "todo-badges");
    badges.append(
      mailElement(
        "span",
        `todo-priority is-${todo.priority}`,
        todoPriorityLabel(todo.priority),
      ),
      mailElement(
        "span",
        "todo-source",
        todo.source === "automatic" ? "Automatisch" : "Manuell",
      ),
    );
    heading.append(titleArea, badges);

    const description = mailElement(
      "p",
      "todo-description",
      todo.description || "Keine Beschreibung.",
    );
    const meta = mailElement("div", "todo-meta");
    if (todo.due_date) {
      const due = mailElement(
        "span",
        "todo-due-date",
        `Fällig: ${formatDate(todo.due_date)}`,
      );
      if (!todo.completed && todo.due_date < toDateInputValue(new Date())) {
        due.classList.add("is-overdue");
      }
      meta.append(due);
    }
    meta.append(
      mailElement(
        "span",
        "",
        `Aktualisiert: ${formatDateTime(todo.updated_at)}`,
      ),
    );

    const links = mailElement("div", "todo-links");
    if (todo.vorgangs_ids.length) {
      links.append(mailElement("strong", "", "Vorgänge:"));
      for (const vorgangsId of todo.vorgangs_ids) {
        const link = mailElement(
          "button",
          "todo-vorgang-link",
          vorgangDisplayLabel(vorgangsId, state.todoVorgaenge),
        );
        link.type = "button";
        link.dataset.openTodoVorgang = vorgangsId;
        link.title = vorgangsId;
        links.append(link);
      }
    } else {
      links.append(
        mailElement("span", "todo-no-links", "Keinem Vorgang zugeordnet"),
      );
    }

    const actions = mailElement("div", "todo-card-actions");
    const editButton = mailElement("button", "", "Bearbeiten");
    editButton.type = "button";
    editButton.dataset.editTodo = todo.todo_id;
    const createButton = mailElement("button", "", "Vorgang erstellen");
    createButton.type = "button";
    createButton.dataset.createVorgangFromTodo = todo.todo_id;
    const deleteButton = mailElement(
      "button",
      "todo-delete",
      "Löschen",
    );
    deleteButton.type = "button";
    deleteButton.dataset.deleteTodo = todo.todo_id;
    actions.append(editButton, createButton, deleteButton);

    card.append(
      completionLabel,
      heading,
      description,
      meta,
      links,
      actions,
    );
    elements.todoList.append(card);
  }
}

function renderTodoVorgangOptions(selectedIds = []) {
  const selected = new Set(selectedIds);
  elements.todoVorgaenge.replaceChildren();
  for (const vorgang of state.todoVorgaenge) {
    const option = document.createElement("option");
    option.value = vorgang.vorgangs_id;
    option.textContent = vorgangOptionLabel(vorgang);
    option.title = vorgang.vorgangs_id;
    option.selected = selected.has(vorgang.vorgangs_id);
    elements.todoVorgaenge.append(option);
  }
}

async function saveTodo(event) {
  event.preventDefault();
  const payload = todoFormPayload();
  const todoId = state.editingTodoId;
  elements.todoSubmit.disabled = true;
  elements.todoCreateVorgang.disabled = true;
  elements.todoFormStatus.textContent = todoId
    ? "To-Do wird gespeichert"
    : "To-Do wird erstellt";
  try {
    await persistTodo(payload, todoId);
    resetTodoForm();
    elements.todoFormStatus.textContent = todoId
      ? "To-Do wurde gespeichert."
      : "To-Do wurde erstellt.";
    await Promise.all([loadTodos(), loadOverview()]);
  } catch (error) {
    elements.todoFormStatus.textContent = "";
    showError(error.message);
  } finally {
    elements.todoSubmit.disabled = false;
    elements.todoCreateVorgang.disabled = false;
  }
}

async function saveTodoAndCreateVorgang() {
  if (state.editingTodoId) {
    showError("Bitte die Bearbeitung erst speichern oder abbrechen.");
    return;
  }
  if (!elements.todoForm.reportValidity()) {
    return;
  }
  const payload = todoFormPayload();
  elements.todoSubmit.disabled = true;
  elements.todoCreateVorgang.disabled = true;
  elements.todoFormStatus.textContent = "To-Do wird erstellt";
  try {
    const todo = await persistTodo(payload);
    resetTodoForm();
    elements.todoFormStatus.textContent = "To-Do wurde erstellt.";
    await Promise.all([loadTodos(), loadOverview()]);
    openVorgangCreateDialog({
      type: "todo",
      id: todo.todo_id,
      title: todo.title || "Neuer Vorgang",
      description: todo.description || "",
    });
  } catch (error) {
    elements.todoFormStatus.textContent = "";
    showError(error.message);
  } finally {
    elements.todoSubmit.disabled = false;
    elements.todoCreateVorgang.disabled = false;
  }
}

function todoFormPayload() {
  return {
    title: elements.todoTitle.value,
    description: elements.todoDescription.value,
    due_date: elements.todoDueDate.value,
    priority: elements.todoPriority.value,
    vorgangs_ids: [...elements.todoVorgaenge.selectedOptions]
      .map((option) => option.value),
  };
}

async function persistTodo(payload, todoId = "") {
  const response = await fetch(
    todoId
      ? `/api/todos/${encodeURIComponent(todoId)}`
      : "/api/todos",
    {
      method: todoId ? "PATCH" : "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload),
    },
  );
  const result = await readResponse(response);
  return result.todo;
}

function editTodo(todoId) {
  const todo = state.todos.find((item) => item.todo_id === todoId);
  if (!todo) {
    return;
  }
  state.editingTodoId = todoId;
  elements.todoFormTitle.textContent = "To-Do bearbeiten";
  elements.todoTitle.value = todo.title;
  elements.todoDescription.value = todo.description;
  elements.todoDueDate.value = todo.due_date || "";
  elements.todoPriority.value = todo.priority;
  elements.todoSubmit.textContent = "Änderungen speichern";
  elements.todoCreateVorgang.hidden = true;
  elements.todoCancelEdit.hidden = false;
  elements.todoFormStatus.textContent = "";
  renderTodoVorgangOptions(todo.vorgangs_ids);
  elements.todoTitle.focus();
}

function resetTodoForm() {
  state.editingTodoId = null;
  elements.todoForm.reset();
  elements.todoPriority.value = "normal";
  elements.todoFormTitle.textContent = "Neues To-Do";
  elements.todoSubmit.textContent = "To-Do erstellen";
  elements.todoCreateVorgang.hidden = false;
  elements.todoCancelEdit.hidden = true;
  elements.todoFormStatus.textContent = "";
  renderTodoVorgangOptions();
}

async function handleTodoListChange(event) {
  const checkbox = event.target.closest("[data-toggle-todo]");
  if (!checkbox) {
    return;
  }
  checkbox.disabled = true;
  try {
    const response = await fetch(
      `/api/todos/${encodeURIComponent(checkbox.dataset.toggleTodo)}`,
      {
        method: "PATCH",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({completed: checkbox.checked}),
      },
    );
    await readResponse(response);
    await Promise.all([loadTodos(), loadOverview()]);
  } catch (error) {
    checkbox.checked = !checkbox.checked;
    checkbox.disabled = false;
    showError(error.message);
  }
}

async function handleTodoListClick(event) {
  const vorgangButton = event.target.closest("[data-open-todo-vorgang]");
  if (vorgangButton) {
    activateTab("vorgaenge");
    await openVorgang(vorgangButton.dataset.openTodoVorgang);
    return;
  }
  const editButton = event.target.closest("[data-edit-todo]");
  if (editButton) {
    editTodo(editButton.dataset.editTodo);
    return;
  }
  const createButton = event.target.closest("[data-create-vorgang-from-todo]");
  if (createButton) {
    const todo = state.todos.find(
      (item) => item.todo_id === createButton.dataset.createVorgangFromTodo,
    );
    openVorgangCreateDialog({
      type: "todo",
      id: createButton.dataset.createVorgangFromTodo,
      title: todo?.title || "Neuer Vorgang",
      description: todo?.description || "",
    });
    return;
  }
  const deleteButton = event.target.closest("[data-delete-todo]");
  if (!deleteButton) {
    return;
  }
  const todo = state.todos.find(
    (item) => item.todo_id === deleteButton.dataset.deleteTodo,
  );
  if (!window.confirm(`To-Do "${todo?.title || ""}" wirklich löschen?`)) {
    return;
  }
  deleteButton.disabled = true;
  try {
    const response = await fetch(
      `/api/todos/${encodeURIComponent(deleteButton.dataset.deleteTodo)}`,
      {method: "DELETE"},
    );
    await readResponse(response);
    if (state.editingTodoId === deleteButton.dataset.deleteTodo) {
      resetTodoForm();
    }
    await Promise.all([loadTodos(), loadOverview()]);
  } catch (error) {
    deleteButton.disabled = false;
    showError(error.message);
  }
}

function todoPriorityLabel(value) {
  return {
    hoch: "Hohe Priorität",
    normal: "Normale Priorität",
    niedrig: "Niedrige Priorität",
  }[value] || value;
}

async function loadTermine() {
  elements.terminLoading.hidden = false;
  elements.terminEmpty.hidden = true;
  const parameters = new URLSearchParams({
    search: state.terminSearch,
    hide_completed: String(state.terminHideCompleted),
    unassigned_upcoming: String(state.terminUnassignedUpcoming),
  });
  try {
    const requests = [fetch(`/api/termine?${parameters}`)];
    if (!state.terminVorgaenge.length) {
      requests.push(fetch("/api/vorgaenge"));
    }
    const responses = await Promise.all(requests);
    const payload = await readResponse(responses[0]);
    if (responses[1]) {
      const vorgangPayload = await readResponse(responses[1]);
      state.terminVorgaenge = vorgangPayload.vorgaenge || [];
      renderTerminVorgangOptions(
        state.editingTerminId
          ? state.termine.find(
            (termin) => termin.termin_id === state.editingTerminId,
          )?.vorgangs_ids || []
          : [],
      );
    }
    state.termine = payload.termine || [];
    state.termineLoaded = true;
    elements.terminCount.textContent = integerFormatter.format(payload.count);
    elements.terminCountLabel.textContent =
      payload.count === 1 ? "Termin" : "Termine";
    renderTerminList();
  } catch (error) {
    state.termine = [];
    renderTerminList();
    showError(error.message);
  } finally {
    elements.terminLoading.hidden = true;
  }
}

function renderTerminList() {
  elements.terminList.replaceChildren();
  elements.terminEmpty.hidden = state.termine.length > 0;
  for (const termin of state.termine) {
    const card = mailElement(
      "article",
      `todo-card termin-card is-${termin.status}`,
    );
    card.dataset.terminId = termin.termin_id;
    const heading = mailElement("div", "todo-card-heading");
    const titleArea = mailElement("div");
    titleArea.append(
      mailElement("h3", "", termin.title),
      mailElement("code", "todo-id", termin.termin_id),
    );
    const badges = mailElement("div", "todo-badges");
    badges.append(
      mailElement("span", "todo-priority is-normal", terminStatusLabel(termin.status)),
      mailElement(
        "span",
        "todo-source",
        termin.source === "automatic" ? "Automatisch" : "Manuell",
      ),
    );
    heading.append(titleArea, badges);

    const description = mailElement(
      "p",
      "todo-description",
      termin.description || "Keine Beschreibung.",
    );
    const meta = mailElement("div", "todo-meta");
    meta.append(
      mailElement("span", "", `Beginn: ${formatDateTime(termin.starts_at)}`),
    );
    if (termin.ends_at) {
      meta.append(
        mailElement("span", "", `Ende: ${formatDateTime(termin.ends_at)}`),
      );
    }
    if (termin.location) {
      meta.append(mailElement("span", "", `Ort: ${termin.location}`));
    }

    const links = mailElement("div", "todo-links");
    if (termin.vorgangs_ids.length) {
      links.append(mailElement("strong", "", "Vorgänge:"));
      for (const vorgangsId of termin.vorgangs_ids) {
        const link = mailElement(
          "button",
          "todo-vorgang-link",
          vorgangDisplayLabel(vorgangsId, state.terminVorgaenge),
        );
        link.type = "button";
        link.dataset.openTerminVorgang = vorgangsId;
        link.title = vorgangsId;
        links.append(link);
      }
    } else {
      links.append(
        mailElement("span", "todo-no-links", "Keinem Vorgang zugeordnet"),
      );
    }

    const actions = mailElement("div", "todo-card-actions");
    const editButton = mailElement("button", "", "Bearbeiten");
    editButton.type = "button";
    editButton.dataset.editTermin = termin.termin_id;
    const createButton = mailElement("button", "", "Vorgang erstellen");
    createButton.type = "button";
    createButton.dataset.createVorgangFromTermin = termin.termin_id;
    const deleteButton = mailElement(
      "button",
      "todo-delete",
      "Löschen",
    );
    deleteButton.type = "button";
    deleteButton.dataset.deleteTermin = termin.termin_id;
    actions.append(editButton, createButton, deleteButton);
    card.append(heading, description, meta, links, actions);
    elements.terminList.append(card);
  }
}

function renderTerminVorgangOptions(selectedIds = []) {
  const selected = new Set(selectedIds);
  elements.terminVorgaenge.replaceChildren();
  for (const vorgang of state.terminVorgaenge) {
    const option = document.createElement("option");
    option.value = vorgang.vorgangs_id;
    option.textContent = vorgangOptionLabel(vorgang);
    option.title = vorgang.vorgangs_id;
    option.selected = selected.has(vorgang.vorgangs_id);
    elements.terminVorgaenge.append(option);
  }
}

function vorgangDisplayLabel(vorgangsId, candidates = []) {
  const match = candidates.find((item) => item.vorgangs_id === vorgangsId);
  if (!match) {
    return vorgangsId;
  }
  return match.titel || match.bezug || match.vorgangstyp || vorgangsId;
}

function vorgangOptionLabel(vorgang) {
  const primary = (
    vorgang.titel
    || vorgang.bezug
    || vorgang.vorgangstyp
    || "Vorgang ohne Titel"
  );
  const details = [
    vorgang.vorgangstyp,
    formatStatus(vorgang.status),
    vorgang.letztes_datum ? formatDate(vorgang.letztes_datum) : "",
  ].filter((value) => value && value !== primary);
  return details.length ? `${primary} · ${details.join(" · ")}` : primary;
}

async function saveTermin(event) {
  event.preventDefault();
  const payload = {
    title: elements.terminTitle.value,
    description: elements.terminDescription.value,
    starts_at: localDateTimeToApiValue(elements.terminStartsAt.value),
    ends_at: localDateTimeToApiValue(elements.terminEndsAt.value),
    location: elements.terminLocation.value,
    status: elements.terminStatus.value,
    vorgangs_ids: [...elements.terminVorgaenge.selectedOptions]
      .map((option) => option.value),
  };
  const terminId = state.editingTerminId;
  elements.terminSubmit.disabled = true;
  elements.terminFormStatus.textContent = terminId
    ? "Termin wird gespeichert"
    : "Termin wird erstellt";
  try {
    const response = await fetch(
      terminId
        ? `/api/termine/${encodeURIComponent(terminId)}`
        : "/api/termine",
      {
        method: terminId ? "PATCH" : "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload),
      },
    );
    await readResponse(response);
    resetTerminForm();
    elements.terminFormStatus.textContent = terminId
      ? "Termin wurde gespeichert."
      : "Termin wurde erstellt.";
    await Promise.all([loadTermine(), loadOverview()]);
    state.vorgaengeLoaded = false;
  } catch (error) {
    elements.terminFormStatus.textContent = "";
    showError(error.message);
  } finally {
    elements.terminSubmit.disabled = false;
  }
}

function editTermin(terminId) {
  const termin = state.termine.find((item) => item.termin_id === terminId);
  if (!termin) {
    return;
  }
  state.editingTerminId = terminId;
  elements.terminFormTitle.textContent = "Termin bearbeiten";
  elements.terminTitle.value = termin.title;
  elements.terminDescription.value = termin.description;
  elements.terminStartsAt.value = apiDateTimeToLocalInput(termin.starts_at);
  elements.terminEndsAt.value = apiDateTimeToLocalInput(termin.ends_at);
  elements.terminLocation.value = termin.location;
  elements.terminStatus.value = termin.status;
  elements.terminSubmit.textContent = "Änderungen speichern";
  elements.terminCancelEdit.hidden = false;
  elements.terminFormStatus.textContent = "";
  renderTerminVorgangOptions(termin.vorgangs_ids);
  elements.terminTitle.focus();
}

function resetTerminForm() {
  state.editingTerminId = null;
  elements.terminForm.reset();
  elements.terminStatus.value = "geplant";
  elements.terminFormTitle.textContent = "Neuer Termin";
  elements.terminSubmit.textContent = "Termin erstellen";
  elements.terminCancelEdit.hidden = true;
  elements.terminFormStatus.textContent = "";
  renderTerminVorgangOptions();
}

async function handleTerminListClick(event) {
  const vorgangButton = event.target.closest("[data-open-termin-vorgang]");
  if (vorgangButton) {
    activateTab("vorgaenge");
    await openVorgang(vorgangButton.dataset.openTerminVorgang);
    return;
  }
  const createButton = event.target.closest("[data-create-vorgang-from-termin]");
  if (createButton) {
    const termin = state.termine.find(
      (item) => item.termin_id === createButton.dataset.createVorgangFromTermin,
    );
    openVorgangCreateDialog({
      type: "termin",
      id: createButton.dataset.createVorgangFromTermin,
      title: termin?.title || "Neuer Vorgang",
      description: termin?.description || "",
    });
    return;
  }
  const editButton = event.target.closest("[data-edit-termin]");
  if (editButton) {
    editTermin(editButton.dataset.editTermin);
    return;
  }
  const deleteButton = event.target.closest("[data-delete-termin]");
  if (!deleteButton) {
    return;
  }
  const termin = state.termine.find(
    (item) => item.termin_id === deleteButton.dataset.deleteTermin,
  );
  if (!window.confirm(`Termin "${termin?.title || ""}" wirklich löschen?`)) {
    return;
  }
  deleteButton.disabled = true;
  try {
    const response = await fetch(
      `/api/termine/${encodeURIComponent(deleteButton.dataset.deleteTermin)}`,
      {method: "DELETE"},
    );
    await readResponse(response);
    if (state.editingTerminId === deleteButton.dataset.deleteTermin) {
      resetTerminForm();
    }
    await Promise.all([loadTermine(), loadOverview()]);
  } catch (error) {
    deleteButton.disabled = false;
    showError(error.message);
  }
}

function terminStatusLabel(value) {
  return {
    geplant: "Geplant",
    abgeschlossen: "Abgeschlossen",
    abgesagt: "Abgesagt",
  }[value] || value;
}

async function loadMails(forceDetailReload = false) {
  const sequence = state.mailLoadSequence + 1;
  state.mailLoadSequence = sequence;
  elements.mailRefresh.disabled = true;
  elements.mailDeleteStatus.textContent = "";
  elements.mailLoading.hidden = false;
  elements.mailEmpty.hidden = true;
  try {
    state.mails = [];
    state.mailDeleteSelections.clear();
    state.mailSummaries.clear();
    state.mailSummaryOpen.clear();
    elements.mailCount.textContent = "0";
    renderMailList();
    clearMailDetail();

    const localParameters = new URLSearchParams({local: "1", limit: "200"});
    const localResponse = await fetch(`/api/mail?${localParameters}`);
    const localPayload = await readResponse(localResponse);
    if (state.mailLoadSequence !== sequence) {
      return;
    }
    appendMailPage(localPayload.messages || []);
    state.mailSpamThreshold = Number(localPayload.spam_threshold ?? 0.7);
    elements.mailSpamThreshold.value = String(
      Math.round(state.mailSpamThreshold * 100),
    );
    state.mailsLoaded = true;
    elements.mailCount.textContent = String(state.mails.length);
    renderMailList();
    if (localPayload.error) {
      showError(localPayload.error);
    }

    let cursor = "";
    do {
      const parameters = new URLSearchParams({limit: "10"});
      if (cursor) {
        parameters.set("cursor", cursor);
      }
      const response = await fetch(`/api/mail?${parameters}`);
      const payload = await readResponse(response);
      if (state.mailLoadSequence !== sequence) {
        return;
      }
      appendMailPage(payload.messages || []);
      if (!localPayload.messages?.length) {
        state.mailSpamThreshold = Number(payload.spam_threshold ?? 0.7);
        elements.mailSpamThreshold.value = String(
          Math.round(state.mailSpamThreshold * 100),
        );
      }
      state.mailsLoaded = true;
      elements.mailCount.textContent = String(state.mails.length);
      renderMailList();
      if (payload.error) {
        showError(payload.error);
      }
      cursor = payload.next_cursor || "";
    } while (cursor);

    if (state.mailLoadSequence !== sequence) {
      return;
    }
    if (
      state.selectedMailId
      && state.mails.some((mail) => mail.id === state.selectedMailId)
    ) {
      if (forceDetailReload) {
        await loadMailDetail(state.selectedMailId);
      } else {
        renderMailDetail();
      }
    }
    loadOverview();
  } catch (error) {
    if (state.mailLoadSequence !== sequence) {
      return;
    }
    const hadVisibleMails = state.mails.length > 0;
    if (hadVisibleMails) {
      renderMailList();
    } else {
      state.mails = [];
      state.mailDeleteSelections.clear();
      elements.mailCount.textContent = "0";
      renderMailList();
      clearMailDetail(error.message);
    }
    showError(error.message);
  } finally {
    if (state.mailLoadSequence === sequence) {
      elements.mailRefresh.disabled = false;
      elements.mailLoading.hidden = true;
      renderMailList();
    }
  }
}

function appendMailPage(messages) {
  const byId = new Map(state.mails.map((mail) => [mail.id, mail]));
  for (const mail of messages) {
    if (!mail.id) {
      continue;
    }
    byId.set(mail.id, {...byId.get(mail.id), ...mail});
  }
  state.mails = [...byId.values()].sort(
    (left, right) =>
      Date.parse(right.receivedAt || "") - Date.parse(left.receivedAt || ""),
  );
}

function renderMailList() {
  const query = state.mailSearch.trim().toLocaleLowerCase("de-DE");
  const mails = query
    ? state.mails.filter((mail) =>
      [
        mail.subject,
        mail.fromName,
        mail.fromAddress,
        mail.preview,
        mail.folderName,
        mail.tag,
        mail.isConversation ? "Mailverlauf Verlauf" : "",
      ].join(" ").toLocaleLowerCase("de-DE").includes(query),
    )
    : state.mails;
  elements.mailList.replaceChildren();
  elements.mailEmpty.hidden = mails.length > 0 || !elements.mailLoading.hidden;
  updateMailDeleteSpamButton();
  updateMailDeleteSelectedButton();
  for (const mail of mails) {
    const card = mailElement("article", "mail-list-item");
    card.classList.toggle("is-selected", mail.id === state.selectedMailId);
    card.classList.toggle(
      "is-delete-selected",
      state.mailDeleteSelections.has(mail.id),
    );
    card.dataset.mailId = mail.id;

    const openButton = mailElement("button", "mail-list-open");
    openButton.type = "button";
    openButton.dataset.openMail = mail.id;
    const heading = mailElement("span", "mail-list-heading");
    heading.append(
      mailElement(
        "strong",
        "",
        mail.subject || "(ohne Betreff)",
      ),
      mailSpamBadge(mail),
    );
    if (mail.isConversation) {
      heading.append(mailThreadBadge(mail));
    }
    const sender = [mail.fromName, mail.fromAddress]
      .filter(Boolean)
      .join(" · ");
    openButton.append(
      heading,
      mailElement("span", "mail-list-sender", sender || "Unbekannt"),
      mailElement("span", "mail-list-preview", mail.preview || ""),
      mailElement(
        "span",
        "mail-list-date",
        [
          formatDateTime(mail.receivedAt),
          mail.folderName,
          mail.isConversation
            ? `Mailverlauf (${mail.conversationMessageCount || 1})`
            : "",
          mail.attachmentCount
            ? `${mail.attachmentCount} Anhang/Anhänge`
            : "",
        ].filter(Boolean).join(" · "),
      ),
      mailElement(
        "span",
        "mail-inbox-id",
        `Inbox-ID: ${mail.inboxId || mail.id}`,
      ),
    );

    const tagButton = mailElement(
      "button",
      `mail-tag is-${mail.tag === "BSV" ? "bsv" : "private"}`,
      mail.tag || "Privat",
    );
    tagButton.type = "button";
    tagButton.dataset.toggleMailTag = mail.id;
    tagButton.title = "Tag durch Klick wechseln";

    const readButton = mailElement(
      "button",
      "mail-mark-read",
      "Gelesen",
    );
    readButton.type = "button";
    readButton.dataset.markMailRead = mail.id;
    readButton.title = mail.isConversation
      ? "Ganzen Mailverlauf als gelesen markieren"
      : "Ohne Öffnen als gelesen markieren";

    const summaryButton = mailElement(
      "button",
      "mail-summary-button",
      mailSummaryButtonText(mail.id),
    );
    summaryButton.type = "button";
    summaryButton.dataset.summarizeMail = mail.id;
    summaryButton.disabled = state.mailSummaryLoading.has(mail.id);
    summaryButton.title = mail.isConversation
      ? "Zusammenfassung und ToDos für ganzen Mailverlauf erstellen"
      : "Zusammenfassung und ToDos erstellen";

    const deletePicker = mailElement("label", "mail-delete-picker");
    const deleteCheckbox = document.createElement("input");
    deleteCheckbox.type = "checkbox";
    deleteCheckbox.dataset.selectMailDelete = mail.id;
    deleteCheckbox.checked = state.mailDeleteSelections.has(mail.id);
    deleteCheckbox.setAttribute(
      "aria-label",
      `${mail.subject || "Mail"} zum Löschen markieren`,
    );
    deletePicker.append(
      deleteCheckbox,
      mailElement("span", "", "Löschen"),
    );

    const actions = mailElement("div", "mail-list-actions");
    actions.append(tagButton, summaryButton, readButton, deletePicker);
    card.append(openButton, actions);
    if (state.mailSummaryOpen.has(mail.id)) {
      const summaryPayload = state.mailSummaries.get(mail.id);
      if (summaryPayload) {
        card.append(renderMailSummaryPanel(summaryPayload));
      }
    }
    elements.mailList.append(card);
  }
}

function mailDeleteCandidates() {
  return state.mails.filter(
    (mail) => Number(mail.spamProbability) > state.mailSpamThreshold,
  );
}

function updateMailDeleteSpamButton() {
  const count = mailDeleteCandidates().length;
  elements.mailDeleteSpam.disabled = count === 0;
  elements.mailDeleteSpam.textContent = count === 0
    ? "Keine Spam-Mails zu löschen"
    : count === 1
      ? "1 Spam-Mail löschen"
      : `${count} Spam-Mails löschen`;
}

function updateMailDeleteSelectedButton() {
  const count = state.mailDeleteSelections.size;
  elements.mailDeleteSelected.disabled = count === 0;
  elements.mailDeleteSelected.textContent = count === 0
    ? "Keine Mails markiert"
    : count === 1
      ? "1 markierte Mail löschen"
      : `${count} markierte Mails löschen`;
}

function mailSpamBadge(mail) {
  const probability = Number(mail.spamProbability || 0);
  const percent = Math.round(probability * 100);
  const label = probability > 0 && percent === 0 ? "<1%" : `${percent}%`;
  const badge = mailElement("span", "mail-spam-score", label);
  badge.classList.add(
    percent > state.mailSpamThreshold * 100
      ? "is-high"
      : percent >= 35
        ? "is-medium"
        : "is-low",
  );
  const source = mail.spamSource === "local_fallback"
    ? "Lokale Spam-Bewertung"
    : "OpenAI-Spam-Bewertung";
  badge.title = [source, ...(mail.spamReasons || [])].join("\n");
  return badge;
}

function mailThreadBadge(mail) {
  const count = Number(mail.conversationMessageCount || 1);
  const badge = mailElement(
    "span",
    "mail-thread-badge",
    count > 1 ? `Verlauf · ${count}` : "Verlauf",
  );
  badge.title = count > 1
    ? "Aktionen werden auf den ganzen Mailverlauf angewendet"
    : "Die Mail enthaelt erkennbar einen Verlauf";
  return badge;
}

function mailSummaryButtonText(entryId) {
  if (state.mailSummaryLoading.has(entryId)) {
    return state.mailSummaries.has(entryId) ? "Wird aktualisiert" : "Wird erstellt";
  }
  return state.mailSummaryOpen.has(entryId)
    ? "Zuklappen"
    : "Zusammenfassung";
}

function refreshMailViews() {
  renderMailList();
  if (state.selectedMailId && state.selectedMailDetail) {
    renderMailDetail();
  }
}

async function handleMailListClick(event) {
  const todoButton = event.target.closest("[data-create-todo-from-summary]");
  if (todoButton) {
    await createTodoFromMailSummary(todoButton);
    return;
  }
  const manualTodoButton = event.target.closest(
    "[data-create-manual-todo-from-summary]",
  );
  if (manualTodoButton) {
    openManualTodoFromMailSummary(manualTodoButton.dataset.createManualTodoFromSummary);
    return;
  }
  const summaryButton = event.target.closest("[data-summarize-mail]");
  if (summaryButton) {
    await toggleMailSummary(
      summaryButton.dataset.summarizeMail,
      summaryButton,
    );
    return;
  }
  const readButton = event.target.closest("[data-mark-mail-read]");
  if (readButton) {
    await markMailRead(readButton.dataset.markMailRead, readButton);
    return;
  }
  const tagButton = event.target.closest("[data-toggle-mail-tag]");
  if (tagButton) {
    await toggleMailTag(tagButton.dataset.toggleMailTag, tagButton);
    return;
  }
  const openButton = event.target.closest("[data-open-mail]");
  if (openButton) {
    await loadMailDetail(openButton.dataset.openMail);
  }
}

async function toggleMailSummary(entryId, button) {
  if (state.mailSummaryOpen.has(entryId)) {
    state.mailSummaryOpen.delete(entryId);
    refreshMailViews();
    return;
  }
  if (state.mailSummaries.has(entryId)) {
    state.mailSummaryOpen.add(entryId);
    refreshMailViews();
    return;
  }

  state.mailSummaryLoading.add(entryId);
  state.mailSummaryOpen.add(entryId);
  if (button) {
    button.disabled = true;
    button.textContent = "Wird erstellt";
  }
  refreshMailViews();
  try {
    await fetchMailSummaryStream(entryId);
  } catch (error) {
    showError(error.message);
  } finally {
    state.mailSummaryLoading.delete(entryId);
    refreshMailViews();
  }
}

async function fetchMailSummaryStream(entryId) {
  const response = await fetch(
    `/api/mail/${encodeURIComponent(entryId)}/summary-stream`,
    {method: "POST"},
  );
  if (!response.ok || !response.body) {
    const finalPayload = await readResponse(response);
    state.mailSummaries.set(entryId, finalPayload);
    return;
  }
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const {value, done} = await reader.read();
    if (done) {
      break;
    }
    buffer += decoder.decode(value, {stream: true});
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";
    for (const line of lines) {
      handleMailSummaryStreamLine(entryId, line);
    }
  }
  if (buffer.trim()) {
    handleMailSummaryStreamLine(entryId, buffer);
  }
}

function handleMailSummaryStreamLine(entryId, line) {
  const cleaned = String(line || "").trim();
  if (!cleaned) {
    return;
  }
  const event = JSON.parse(cleaned);
  if (event.type === "summary" && event.payload) {
    state.mailSummaries.set(entryId, event.payload);
    refreshMailViews();
    return;
  }
  if (event.type === "error") {
    throw new Error(event.error || "Zusammenfassung fehlgeschlagen.");
  }
}

function renderMailSummaryPanel(payload, className = "") {
  const summary = payload.summary || {};
  const panel = mailElement(
    "section",
    ["mail-summary-panel", className].filter(Boolean).join(" "),
  );
  const header = mailElement("div", "mail-summary-header");
  const source = summary.source === "local_fallback"
    ? "Lokale Kurzübersicht"
    : "OpenAI-Zusammenfassung";
  const conversation = payload.conversation || {};
  const sourceParts = [
    payload.cached ? `${source} · gespeichert` : source,
    conversation.isConversation
      ? `${conversation.messageCount || 1} Nachrichten`
      : "",
  ].filter(Boolean);
  header.append(
    mailElement("strong", "", summary.title || "Zusammenfassung"),
    mailElement(
      "span",
      "mail-summary-source",
      sourceParts.join(" · "),
    ),
  );
  panel.append(
    header,
    mailElement(
      "p",
      "mail-summary-text",
      summary.summary || "Keine Zusammenfassung verfügbar.",
    ),
  );

  appendMailSummaryList(
    panel,
    "Wichtige Punkte",
    summary.importantPoints || [],
  );
  appendMailSummaryList(
    panel,
    "Anhänge",
    summary.attachments || [],
  );

  const actionItems = summary.actionItems || [];
  const christophItems = actionItems.filter(
    (item) => item.isForChristoph,
  );
  const christophSection = mailElement(
    "section",
    "mail-summary-todos is-christoph",
  );
  christophSection.append(
    mailElement("h4", "", "ToDos für Christoph Süßmeier"),
  );
  if (christophItems.length) {
    const list = mailElement("ul");
    for (const item of christophItems) {
      const itemIndex = actionItems.indexOf(item);
      list.append(renderMailTodo(item, payload.id, itemIndex));
    }
    christophSection.append(list);
  } else {
    christophSection.append(
      mailElement(
        "p",
        "mail-summary-empty",
        "Keine Aufgabe ist dir eindeutig zugeordnet.",
      ),
    );
  }
  panel.append(christophSection);

  const otherItems = actionItems.filter((item) => !item.isForChristoph);
  if (otherItems.length) {
    const otherSection = mailElement("section", "mail-summary-todos");
    otherSection.append(mailElement("h4", "", "Weitere oder unklare ToDos"));
    const list = mailElement("ul");
    for (const item of otherItems) {
      const itemIndex = actionItems.indexOf(item);
      list.append(renderMailTodo(item, payload.id, itemIndex));
    }
    otherSection.append(list);
    panel.append(otherSection);
  }
  const actions = mailElement("div", "mail-summary-actions");
  const manualTodo = mailElement(
    "button",
    "secondary-action",
    "Manuelles To-Do",
  );
  manualTodo.type = "button";
  manualTodo.dataset.createManualTodoFromSummary = payload.id || "";
  actions.append(manualTodo);
  panel.append(actions);
  if (summary.notice) {
    panel.append(mailElement("p", "mail-summary-notice", summary.notice));
  }
  return panel;
}

function renderMailSummaryLoadingPanel() {
  const panel = mailElement("section", "mail-summary-panel is-detail");
  panel.append(
    mailElement("strong", "", "Zusammenfassung"),
    mailElement("p", "mail-summary-text", "Zusammenfassung wird erstellt."),
  );
  return panel;
}

function appendMailSummaryList(panel, title, values) {
  if (!values.length) {
    return;
  }
  const section = mailElement("section", "mail-summary-list");
  section.append(mailElement("h4", "", title));
  const list = mailElement("ul");
  for (const value of values) {
    list.append(mailElement("li", "", value));
  }
  section.append(list);
  panel.append(section);
}

function renderMailTodo(item, entryId = "", itemIndex = -1) {
  const listItem = mailElement("li");
  const task = mailElement("span", "mail-summary-task", item.task || "");
  const metaParts = [
    item.person ? `Zuständig: ${item.person}` : "",
    item.due ? `Fällig: ${item.due}` : "",
  ].filter(Boolean);
  listItem.append(task);
  if (metaParts.length) {
    listItem.append(
      mailElement("small", "mail-summary-todo-meta", metaParts.join(" · ")),
    );
  }
  const actions = mailElement("div", "mail-summary-todo-actions");
  const createButton = mailElement("button", "secondary-action", "To-Do erstellen");
  createButton.type = "button";
  createButton.dataset.createTodoFromSummary = entryId;
  createButton.dataset.summaryTodoIndex = String(itemIndex);
  actions.append(createButton);
  listItem.append(actions);
  return listItem;
}

async function createTodoFromMailSummary(button) {
  const entryId = button.dataset.createTodoFromSummary;
  const index = Number(button.dataset.summaryTodoIndex);
  const payload = state.mailSummaries.get(entryId);
  const item = payload?.summary?.actionItems?.[index];
  if (!item?.task) {
    showError("To-Do-Vorschlag wurde nicht gefunden.");
    return;
  }
  button.disabled = true;
  button.textContent = "Wird erstellt";
  try {
    await persistTodo({
      title: item.task.slice(0, 300),
      description: mailSummaryTodoDescription(entryId, item),
      due_date: isoDateOrBlank(item.due),
      priority: item.isForChristoph ? "hoch" : "normal",
      vorgangs_ids: [],
    });
    state.todosLoaded = false;
    await Promise.all([loadOverview(), loadTodos().catch(() => null)]);
    button.textContent = "Erstellt";
  } catch (error) {
    button.disabled = false;
    button.textContent = "To-Do erstellen";
    showError(error.message);
  }
}

function openManualTodoFromMailSummary(entryId) {
  const payload = state.mailSummaries.get(entryId);
  resetTodoForm();
  const summary = payload?.summary || {};
  const mail = state.mails.find((item) => item.id === entryId);
  elements.todoTitle.value = "";
  elements.todoDescription.value = [
    mail?.subject ? `Mail: ${mail.subject}` : "",
    summary.summary ? `Zusammenfassung: ${summary.summary}` : "",
  ].filter(Boolean).join("\n\n");
  activateTab("todos");
  elements.todoTitle.focus();
}

function mailSummaryTodoDescription(entryId, item) {
  const mail = state.mails.find((entry) => entry.id === entryId);
  return [
    item.person ? `Zuständig: ${item.person}` : "",
    item.due ? `Fällig: ${item.due}` : "",
    mail?.subject ? `Aus Mail: ${mail.subject}` : "",
  ].filter(Boolean).join("\n");
}

function isoDateOrBlank(value) {
  const match = String(value || "").match(/\b\d{4}-\d{2}-\d{2}\b/);
  return match ? match[0] : "";
}

function handleMailSelectionChange(event) {
  const checkbox = event.target.closest("[data-select-mail-delete]");
  if (!checkbox) {
    return;
  }
  const entryId = checkbox.dataset.selectMailDelete;
  if (checkbox.checked) {
    state.mailDeleteSelections.add(entryId);
  } else {
    state.mailDeleteSelections.delete(entryId);
  }
  checkbox.closest(".mail-list-item")?.classList.toggle(
    "is-delete-selected",
    checkbox.checked,
  );
  updateMailDeleteSelectedButton();
}

async function markMailRead(entryId, button) {
  button.disabled = true;
  button.textContent = "Wird gelesen";
  try {
    const response = await fetch(
      `/api/mail/${encodeURIComponent(entryId)}/read`,
      {method: "POST"},
    );
    const payload = await readResponse(response);
    const affectedIds = mailAffectedIds(payload, entryId);
    state.mails = state.mails.filter((mail) => !affectedIds.has(mail.id));
    for (const id of affectedIds) {
      state.mailDeleteSelections.delete(id);
    }
    elements.mailCount.textContent = String(state.mails.length);
    elements.mailDeleteStatus.textContent =
      affectedIds.size > 1
        ? "Mailverlauf wurde als gelesen markiert."
        : "Mail wurde als gelesen markiert.";
    if (affectedIds.has(state.selectedMailId)) {
      clearMailDetail(
        affectedIds.size > 1
          ? "Mailverlauf wurde als gelesen markiert."
          : "Mail wurde als gelesen markiert.",
      );
    } else {
      renderMailList();
    }
    loadOverview();
  } catch (error) {
    button.disabled = false;
    button.textContent = "Gelesen";
    showError(error.message);
  }
}

async function loadMailDetail(entryId) {
  state.selectedMailId = entryId;
  state.selectedMailDetail = null;
  state.selectedMailAttachment = null;
  state.mailVorgangReview = null;
  state.mailVorgangSearch = "";
  state.mailVorgangHideCompleted = false;
  state.mailZoom = 1;
  renderMailList();
  elements.mailDetail.replaceChildren(
    mailElement("div", "mail-detail-loading", "Mail wird geladen"),
  );
  try {
    const [response, linksResponse, vorgaengeResponse] = await Promise.all([
      fetch(`/api/mail/${encodeURIComponent(entryId)}`),
      fetch(`/api/mail/${encodeURIComponent(entryId)}/vorgaenge`),
      fetch("/api/vorgaenge"),
    ]);
    const payload = await readResponse(response);
    const linksPayload = await readResponse(linksResponse);
    const vorgaengePayload = await readResponse(vorgaengeResponse);
    state.selectedMailDetail = {
      ...payload.message,
      vorgangs_ids: linksPayload.vorgangs_ids || [],
      vorgaenge: linksPayload.vorgaenge || [],
    };
    state.mailVorgangCandidates = vorgaengePayload.vorgaenge || [];
    const firstAttachment = payload.message.attachments?.[0];
    state.selectedMailAttachment = firstAttachment
      ? firstAttachment.attachmentIndex
      : null;
    renderMailDetail();
  } catch (error) {
    clearMailDetail(error.message);
    showError(error.message);
  }
}

function renderMailDetail() {
  const detail = state.selectedMailDetail;
  const summary = state.mails.find(
    (mail) => mail.id === state.selectedMailId,
  );
  if (!detail || !summary) {
    clearMailDetail();
    return;
  }
  elements.mailDetail.replaceChildren();

  const header = mailElement("header", "mail-detail-header");
  const titleArea = mailElement("div");
  titleArea.append(
    mailElement("p", "eyebrow", "Mailinhalt"),
    mailElement("h3", "", detail.subject || "(ohne Betreff)"),
    mailElement(
      "p",
      "mail-detail-meta",
      [
        [detail.fromName, detail.fromAddress].filter(Boolean).join(" · "),
        formatDateTime(detail.receivedDateTime),
        (detail.recipients || []).length
          ? `An: ${detail.recipients.join(", ")}`
          : "",
        detail.isConversation
          ? `Mailverlauf: ${detail.conversationMessageCount || 1} Nachricht(en)`
          : "",
        `Inbox-ID: ${detail.inboxId || detail.id}`,
      ].filter(Boolean).join("\n"),
    ),
  );
  const actions = mailElement("div", "mail-detail-actions");
  const tagButton = mailElement(
    "button",
    `mail-tag is-${summary.tag === "BSV" ? "bsv" : "private"}`,
    summary.tag,
  );
  tagButton.type = "button";
  tagButton.dataset.toggleMailTag = summary.id;
  tagButton.title = "Tag durch Klick wechseln";
  const deleteButton = mailElement(
    "button",
    "mail-delete-button",
    "Löschen",
  );
  deleteButton.type = "button";
  deleteButton.dataset.deleteMail = summary.id;
  deleteButton.title = summary.isConversation
    ? "Ganzen Mailverlauf löschen"
    : "Mail löschen";
  const createVorgangButton = mailElement(
    "button",
    "primary-action",
    "Vorgang erstellen",
  );
  createVorgangButton.type = "button";
  createVorgangButton.dataset.mailCreateVorgang = summary.id;
  const createTerminButton = mailElement(
    "button",
    "secondary-action",
    "Termin erstellen",
  );
  createTerminButton.type = "button";
  createTerminButton.dataset.mailCreateTermin = summary.id;
  const summaryButton = mailElement(
    "button",
    "mail-summary-button",
    mailSummaryButtonText(summary.id),
  );
  summaryButton.type = "button";
  summaryButton.dataset.summarizeMail = summary.id;
  summaryButton.disabled = state.mailSummaryLoading.has(summary.id);
  const readButton = mailElement("button", "mail-mark-read", "Gelesen");
  readButton.type = "button";
  readButton.dataset.markMailRead = summary.id;
  readButton.title = summary.isConversation
    ? "Ganzen Mailverlauf als gelesen markieren"
    : "Mail als gelesen markieren";
  actions.append(
    mailSpamBadge(summary),
    tagButton,
    createVorgangButton,
    createTerminButton,
    summaryButton,
    readButton,
    deleteButton,
  );
  header.append(titleArea, actions);

  const summaryPayload = state.mailSummaries.get(summary.id);
  const summaryPanel = state.mailSummaryOpen.has(summary.id)
    ? (
      summaryPayload
        ? renderMailSummaryPanel(summaryPayload, "is-detail")
        : renderMailSummaryLoadingPanel()
    )
    : null;
  const relatedPanel = renderRelatedMailCandidates(
    detail.relatedCandidates || [],
  );
  const vorgangSection = renderMailVorgangSection(detail);

  const readingLayout = mailElement("div", "mail-reading-layout");
  const bodySection = mailElement("section", "mail-body-pane");
  bodySection.append(
    mailElement("h4", "", "Mail"),
    mailElement(
      "pre",
      "mail-body-text",
      detail.body || "(kein Textinhalt)",
    ),
  );
  const attachmentSection = renderMailAttachmentPane(detail);
  readingLayout.append(bodySection, attachmentSection);

  const replyForm = mailElement("form", "mail-reply-form");
  replyForm.dataset.mailReplyForm = summary.id;
  const recipientLabel = mailElement("label");
  recipientLabel.append(
    mailElement("span", "", "An"),
  );
  const recipientInput = document.createElement("input");
  recipientInput.name = "to_recipients";
  recipientInput.type = "text";
  recipientInput.required = true;
  recipientInput.value = defaultReplyRecipients(detail, summary).join(", ");
  recipientInput.placeholder = "mail@example.org, zweite@example.org";
  recipientLabel.append(recipientInput);
  const replyLabel = mailElement("label");
  replyLabel.append(
    mailElement("span", "", "Antwort"),
  );
  const textarea = document.createElement("textarea");
  textarea.name = "body";
  textarea.rows = 5;
  textarea.maxLength = 50000;
  textarea.required = true;
  textarea.placeholder = "Antworttext eingeben";
  replyLabel.append(textarea);
  const replyActions = mailElement("div", "mail-reply-actions");
  const replyButton = mailElement(
    "button",
    "primary-action",
    "Antwort senden",
  );
  replyButton.type = "submit";
  replyActions.append(
    replyButton,
    mailElement("span", "mail-reply-status"),
  );
  replyForm.append(recipientLabel, replyLabel, replyActions);
  const nodes = [header, readingLayout];
  if (summaryPanel) {
    nodes.splice(1, 0, summaryPanel);
  }
  if (relatedPanel) {
    nodes.splice(summaryPanel ? 2 : 1, 0, relatedPanel);
  }
  nodes.push(vorgangSection);
  nodes.push(replyForm);
  elements.mailDetail.append(...nodes);
  applyMailZoom();
}

function defaultReplyRecipients(detail, summary) {
  const candidates = [
    detail?.fromAddress,
    detail?.from?.emailAddress?.address,
    summary?.fromAddress,
  ];
  const recipients = [];
  const seen = new Set();
  for (const candidate of candidates) {
    const value = String(candidate || "").trim();
    if (!value || seen.has(value.toLowerCase())) {
      continue;
    }
    seen.add(value.toLowerCase());
    recipients.push(value);
  }
  return recipients;
}

function renderMailVorgangSection(detail) {
  const section = mailElement("section", "mail-vorgang-links");
  section.append(
    mailElement("p", "eyebrow", "Zuordnung"),
    mailElement("h4", "", "Verknüpfte Vorgänge"),
  );
  const linked = dedupeVorgaenge(detail.vorgaenge || []);
  const list = mailElement("div", "mail-vorgang-list");
  if (linked.length) {
    for (const vorgang of linked) {
      const row = mailElement("div", "mail-vorgang-item");
      const text = mailElement("div");
      text.append(
        mailElement(
          "strong",
          "",
          vorgang.titel || vorgang.bezug || vorgang.vorgangs_id,
        ),
        mailElement(
          "span",
          "",
          [
            vorgang.vorgangs_id,
            vorgang.vorgangstyp,
            formatStatus(vorgang.status),
          ].filter(Boolean).join(" · "),
        ),
      );
      const actions = mailElement("div", "mail-vorgang-actions");
      const openButton = mailElement("button", "", "Öffnen");
      openButton.type = "button";
      openButton.dataset.openVorgang = vorgang.vorgangs_id;
      const unlinkButton = mailElement("button", "secondary-action", "Entfernen");
      unlinkButton.type = "button";
      unlinkButton.dataset.unlinkMailVorgang = vorgang.vorgangs_id;
      actions.append(openButton, unlinkButton);
      row.append(text, actions);
      list.append(row);
    }
  } else {
    list.append(
      mailElement("p", "mail-vorgang-empty", "Noch keinem Vorgang zugeordnet."),
    );
  }
  section.append(list);

  const form = mailElement("form", "mail-vorgang-form");
  form.dataset.linkMailVorgang = detail.id || detail.inboxId || state.selectedMailId;
  const controls = mailElement("div", "mail-vorgang-search-controls");
  const searchLabel = mailElement("label", "mail-vorgang-search");
  searchLabel.append(mailElement("span", "", "Vorhandene Vorgänge suchen"));
  const search = document.createElement("input");
  search.type = "search";
  search.autocomplete = "off";
  search.placeholder = "Titel, Bezug oder Beschreibung";
  search.value = state.mailVorgangSearch;
  search.dataset.mailVorgangSearch = "";
  searchLabel.append(search);
  const hideCompleted = mailElement("label", "mail-vorgang-filter");
  const hideCompletedInput = document.createElement("input");
  hideCompletedInput.type = "checkbox";
  hideCompletedInput.checked = state.mailVorgangHideCompleted;
  hideCompletedInput.dataset.mailVorgangHideCompleted = "";
  hideCompleted.append(
    hideCompletedInput,
    mailElement("span", "", "Abgeschlossene ausblenden"),
  );
  controls.append(searchLabel, hideCompleted);
  const results = mailElement("div", "mail-vorgang-candidate-list");
  results.dataset.mailVorgangResults = "";
  form.append(controls, results);
  renderMailVorgangCandidateResults(form);
  const formActions = mailElement("div", "mail-vorgang-form-actions");
  const submit = mailElement("button", "primary-action", "Zuordnung bestätigen");
  submit.type = "submit";
  formActions.append(submit, mailElement("span", "save-state"));
  form.append(formActions);
  section.append(form);
  return section;
}

function mailVorgangAvailableCandidates(detail = state.selectedMailDetail) {
  const linkedIds = new Set(
    dedupeVorgaenge(detail?.vorgaenge || []).map((item) => item.vorgangs_id),
  );
  return state.mailVorgangCandidates.filter(
    (vorgang) => vorgang?.vorgangs_id && !linkedIds.has(vorgang.vorgangs_id),
  );
}

function renderMailVorgangCandidateResults(form) {
  const results = form.querySelector("[data-mail-vorgang-results]");
  if (!results) {
    return;
  }
  const available = mailVorgangAvailableCandidates();
  results.replaceChildren();
  if (!available.length) {
    const message = state.mailVorgangSearch
      ? "Keine Vorgänge zur Suche gefunden."
      : "Keine weiteren Vorgänge verfügbar.";
    results.append(mailElement("p", "mail-vorgang-empty", message));
    setMailVorgangSubmitState(form);
    return;
  }
  for (const vorgang of available) {
    const row = mailElement("label", "mail-vorgang-candidate");
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "vorgangs_id";
    radio.value = vorgang.vorgangs_id;
    const text = mailElement("span");
    text.append(
      mailElement("strong", "", vorgang.titel || vorgang.bezug || vorgang.vorgangs_id),
      mailElement(
        "small",
        "",
        [
          formatStatus(vorgang.status),
          vorgang.vorgangstyp,
          vorgang.bezug,
          Number.isFinite(Number(vorgang.anzahl_transaktionen))
            ? `${integerFormatter.format(Number(vorgang.anzahl_transaktionen))} Transaktionen`
            : "",
        ].filter(Boolean).join(" · "),
      ),
    );
    row.append(radio, text);
    results.append(row);
  }
  setMailVorgangSubmitState(form);
}

function setMailVorgangSubmitState(form) {
  const submit = form.querySelector('button[type="submit"]');
  if (!submit) {
    return;
  }
  submit.disabled = form.dataset.assignmentSaving === "true";
}

async function loadMailVorgangCandidates() {
  const detail = state.selectedMailDetail;
  if (!detail) {
    return;
  }
  if (state.mailVorgangRequest) {
    state.mailVorgangRequest.abort();
  }
  state.mailVorgangRequest = new AbortController();
  const form = elements.mailDetail.querySelector("[data-link-mail-vorgang]");
  const status = form?.querySelector(".save-state");
  if (status) {
    status.className = "save-state is-saving";
    status.textContent = "Vorgänge werden gesucht";
  }
  const parameters = new URLSearchParams({
    search: state.mailVorgangSearch,
    hide_completed: String(state.mailVorgangHideCompleted),
  });
  try {
    const response = await fetch(`/api/vorgaenge?${parameters}`, {
      signal: state.mailVorgangRequest.signal,
    });
    const payload = await readResponse(response);
    state.mailVorgangCandidates = payload.vorgaenge || [];
    if (form) {
      renderMailVorgangCandidateResults(form);
    }
    if (status) {
      status.className = "save-state";
      status.textContent = "";
    }
  } catch (error) {
    if (error.name === "AbortError") {
      return;
    }
    if (status) {
      status.className = "save-state is-error";
      status.textContent = "Suche fehlgeschlagen";
    }
    showError(error.message);
  }
}

function dedupeVorgaenge(vorgaenge) {
  const byId = new Map();
  for (const vorgang of vorgaenge) {
    if (vorgang?.vorgangs_id && !byId.has(vorgang.vorgangs_id)) {
      byId.set(vorgang.vorgangs_id, vorgang);
    }
  }
  return [...byId.values()];
}

function renderRelatedMailCandidates(candidates) {
  if (!candidates.length) {
    return null;
  }
  const section = mailElement("section", "mail-related-candidates");
  section.append(
    mailElement("p", "eyebrow", "Möglicher Zusammenhang"),
    mailElement("h4", "", "Ähnliche ungelesene Mails"),
  );
  const list = mailElement("div", "mail-related-list");
  for (const candidate of candidates) {
    const button = mailElement("button", "mail-related-item");
    button.type = "button";
    button.dataset.openMail = candidate.id;
    button.append(
      mailElement("strong", "", candidate.subject || "(ohne Betreff)"),
      mailElement(
        "span",
        "",
        [
          formatDateTime(candidate.receivedAt),
          candidate.reason,
          candidate.confidence
            ? `${Math.round(Number(candidate.confidence) * 100)}%`
            : "",
        ].filter(Boolean).join(" · "),
      ),
    );
    list.append(button);
  }
  section.append(list);
  return section;
}

function renderMailAttachmentPane(detail) {
  const pane = mailElement("aside", "mail-attachment-pane");
  const attachments = detail.attachments || [];
  const heading = mailElement("div", "mail-attachment-heading");
  heading.append(
    mailElement(
      "h4",
      "",
      `Anhänge (${attachments.length})`,
    ),
  );
  if (!attachments.length) {
    pane.append(heading, mailElement("p", "mail-no-attachment", "Keine Anhänge"));
    return pane;
  }

  const zoom = mailElement("div", "mail-zoom-controls");
  const zoomOut = mailElement("button", "", "−");
  zoomOut.type = "button";
  zoomOut.dataset.mailZoomDelta = "-0.25";
  zoomOut.title = "Verkleinern";
  const range = document.createElement("input");
  range.type = "range";
  range.min = "25";
  range.max = "800";
  range.step = "25";
  range.value = String(Math.round(state.mailZoom * 100));
  range.dataset.mailZoomRange = "";
  const zoomIn = mailElement("button", "", "+");
  zoomIn.type = "button";
  zoomIn.dataset.mailZoomDelta = "0.25";
  zoomIn.title = "Vergrößern";
  const zoomValue = mailElement(
    "button",
    "mail-zoom-value",
    `${Math.round(state.mailZoom * 100)}%`,
  );
  zoomValue.type = "button";
  zoomValue.dataset.mailZoomReset = "";
  zoom.append(zoomOut, range, zoomIn, zoomValue);
  heading.append(zoom);

  const picker = mailElement("div", "mail-attachment-picker");
  for (const attachment of attachments) {
    const button = mailElement(
      "button",
      "mail-attachment-choice",
    );
    button.type = "button";
    button.dataset.mailAttachment = String(attachment.attachmentIndex);
    button.classList.toggle(
      "is-selected",
      attachment.attachmentIndex === state.selectedMailAttachment,
    );
    button.append(
      mailElement("strong", "", attachment.filename),
      mailElement(
        "span",
        "",
        [
          attachment.contentType,
          formatFileSize(attachment.size),
        ].filter(Boolean).join(" · "),
      ),
    );
    picker.append(button);
  }
  const stage = mailElement("div", "mail-attachment-stage");
  stage.dataset.mailAttachmentStage = "";
  const preview = mailElement("div", "mail-attachment-preview");
  preview.dataset.mailAttachmentPreview = "";
  stage.append(preview);
  pane.append(heading, picker, stage);
  renderSelectedMailAttachment(preview, detail);
  return pane;
}

function renderSelectedMailAttachment(preview, detail) {
  const attachment = (detail.attachments || []).find(
    (item) => item.attachmentIndex === state.selectedMailAttachment,
  );
  preview.replaceChildren();
  if (!attachment) {
    preview.append(
      mailElement("p", "mail-no-attachment", "Anhang auswählen"),
    );
    return;
  }
  const url = `/api/mail/${encodeURIComponent(detail.id)}/attachments/${
    attachment.attachmentIndex
  }`;
  const content = mailElement("div", "mail-preview-content");
  content.dataset.mailPreviewContent = "";
  const kind = attachmentPreviewKind(attachment);
  if (kind === "image") {
    const image = document.createElement("img");
    image.src = url;
    image.alt = attachment.filename;
    content.append(image);
  } else if (kind === "pdf") {
    const frame = document.createElement("iframe");
    frame.src = url;
    frame.title = attachment.filename;
    content.append(frame);
  } else {
    content.append(
      mailElement(
        "pre",
        "mail-attachment-text",
        attachmentPreviewText(attachment, kind),
      ),
    );
  }
  const openLink = document.createElement("a");
  openLink.href = url;
  openLink.target = "_blank";
  openLink.rel = "noopener";
  if (kind === "office") {
    openLink.download = attachment.filename || "";
  }
  openLink.textContent = kind === "office"
    ? "Original herunterladen"
    : "Original in neuem Fenster öffnen";
  preview.append(content, openLink);
}

function attachmentPreviewKind(attachment) {
  const contentType = String(attachment.contentType || "").toLowerCase();
  const filename = String(attachment.filename || "").toLowerCase();
  if (contentType.startsWith("image/")) {
    return "image";
  }
  if (contentType === "application/pdf" || filename.endsWith(".pdf")) {
    return "pdf";
  }
  if (
    filename.endsWith(".docx")
    || filename.endsWith(".xlsx")
    || filename.endsWith(".pptx")
    || contentType.includes("officedocument")
    || contentType.includes("ms-excel")
    || contentType.includes("msword")
  ) {
    return "office";
  }
  if (contentType.startsWith("text/")) {
    return "text";
  }
  return "other";
}

function attachmentPreviewText(attachment, kind) {
  const text = String(attachment.text || "").trim();
  if (text) {
    return text;
  }
  if (kind === "office") {
    return "Für diese Office-Datei ist keine direkte Vorschau verfügbar. Das Original kann heruntergeladen werden.";
  }
  return "Keine Textvorschau verfügbar.";
}

async function startMailVorgangReview(entryId, button) {
  button.disabled = true;
  button.textContent = "Analyse läuft";
  try {
    const [response, , suggestions, candidates, optionsResponse] = await Promise.all([
      fetch(
        `/api/mail/${encodeURIComponent(entryId)}/vorgang-analysis`,
        {method: "POST"},
      ),
      loadVorgangTypes(),
      loadVorgangSuggestions("mail", entryId).catch(() => null),
      loadLinkCandidates(true),
      fetch("/api/classification-options"),
    ]);
    const [payload, options] = await Promise.all([
      readResponse(response),
      readResponse(optionsResponse),
    ]);
    state.classificationOptions = options;
    state.mailVorgangReview = {
      entryId,
      analysis: payload.analysis,
    };
    openMailVorgangReviewDialog(
      entryId,
      payload.analysis,
      suggestions,
      candidates,
    );
  } catch (error) {
    showError(error.message);
  } finally {
    button.disabled = false;
    button.textContent = "Vorgang erstellen";
  }
}

async function startMailTerminSuggestion(entryId, button) {
  button.disabled = true;
  button.textContent = "Analyse läuft";
  openMailTerminDialog(entryId);
  try {
    const response = await fetch(
      `/api/mail/${encodeURIComponent(entryId)}/termin-suggestion`,
      {method: "POST"},
    );
    const payload = await readResponse(response);
    applyMailTerminSuggestion(entryId, payload.termin || {});
  } catch (error) {
    const form = mailTerminForm(entryId);
    const status = form?.querySelector(".save-state");
    if (status) {
      status.className = "save-state is-error";
      status.textContent = "KI-Vorschlag konnte nicht geladen werden";
    }
    showError(error.message);
  } finally {
    button.disabled = false;
    button.textContent = "Termin erstellen";
  }
}

function openMailTerminDialog(entryId) {
  const detail = state.selectedMailDetail;
  const summary = state.mails.find((mail) => mail.id === entryId);
  elements.dialog.classList.remove("is-vorgang", "has-rule-workspace");
  delete elements.dialog.dataset.vorgangId;
  delete elements.dialog.dataset.vorgangTransactionCount;
  elements.detailEyebrow.textContent = "Termin aus Mail";
  elements.detailTitle.textContent = "Termin erstellen";
  elements.detailSubtitle.textContent =
    "KI-Vorschlag wird geladen und kann direkt angepasst werden";
  elements.detailContent.replaceChildren(
    renderMailTerminForm(
      entryId,
      {
        title: "",
        description: detail?.body || summary?.preview || "",
        starts_at: "",
        ends_at: "",
        location: "",
      },
      true,
    ),
  );
  if (!elements.dialog.open) {
    elements.dialog.showModal();
  }
}

function renderMailTerminForm(entryId, termin, loading = false) {
  const form = mailElement("form", "vorgang-create-form mail-termin-form");
  form.dataset.mailTerminForm = entryId;
  const section = mailElement("section", "detail-section");
  section.append(mailElement("h3", "", "Termindaten"));
  const grid = mailElement("div", "detail-grid");
  grid.append(
    formTextField("Titel", "title", termin.title || "", true),
    formTextField(
      "Beschreibung",
      "description",
      termin.description || "",
      false,
      true,
    ),
    compactInputField(
      "Beginn",
      "starts_at",
      apiDateTimeToLocalInput(termin.starts_at || ""),
      "datetime-local",
    ),
    compactInputField(
      "Ende",
      "ends_at",
      apiDateTimeToLocalInput(termin.ends_at || ""),
      "datetime-local",
    ),
    compactInputField("Ort", "location", termin.location || ""),
  );
  grid.querySelector('[name="starts_at"]').required = true;
  for (const field of grid.querySelectorAll("input, textarea")) {
    field.addEventListener("input", () => {
      field.dataset.userEdited = "true";
    }, {once: true});
  }
  section.append(grid);

  const actions = mailElement("div", "vorgang-form-actions");
  const submit = mailElement("button", "primary-action", "Termin erstellen");
  submit.type = "submit";
  const cancel = mailElement("button", "secondary-action", "Abbrechen");
  cancel.type = "button";
  cancel.addEventListener("click", () => {
    if (elements.dialog.open) {
      elements.dialog.close();
    }
  });
  const status = mailElement(
    "span",
    loading ? "save-state is-saving" : "save-state",
    loading ? "KI-Vorschlag wird geladen" : "",
  );
  actions.append(submit, cancel, status);
  form.append(section, actions);
  form.addEventListener("submit", submitMailTerminForm);
  return form;
}

function mailTerminForm(entryId) {
  return [...document.querySelectorAll("[data-mail-termin-form]")]
    .find((form) => form.dataset.mailTerminForm === entryId) || null;
}

function applyMailTerminSuggestion(entryId, termin) {
  const form = mailTerminForm(entryId);
  if (!form) {
    return;
  }
  setUneditedFieldValue(form.elements.title, termin.title || "");
  setUneditedFieldValue(form.elements.description, termin.description || "");
  setUneditedFieldValue(
    form.elements.starts_at,
    apiDateTimeToLocalInput(termin.starts_at || ""),
  );
  setUneditedFieldValue(
    form.elements.ends_at,
    apiDateTimeToLocalInput(termin.ends_at || ""),
  );
  setUneditedFieldValue(form.elements.location, termin.location || "");
  const status = form.querySelector(".save-state");
  status.className = "save-state is-saved";
  status.textContent = termin.starts_at
    ? "KI-Vorschlag übernommen"
    : "KI-Vorschlag übernommen. Beginn ergänzen.";
  if (!form.elements.title.value) {
    form.elements.title.focus();
  }
}

function setUneditedFieldValue(field, value) {
  if (!field || field.dataset.userEdited === "true") {
    return;
  }
  field.value = value || "";
}

async function submitMailTerminForm(event) {
  event.preventDefault();
  const form = event.target.closest("[data-mail-termin-form]");
  const submit = form.querySelector("button[type='submit']");
  const status = form.querySelector(".save-state");
  submit.disabled = true;
  status.className = "save-state is-saving";
  status.textContent = "Termin wird erstellt";
  try {
    const response = await fetch("/api/termine", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        title: form.elements.title.value,
        description: form.elements.description.value,
        starts_at: localDateTimeToApiValue(form.elements.starts_at.value),
        ends_at: localDateTimeToApiValue(form.elements.ends_at.value),
        location: form.elements.location.value,
        status: "geplant",
        vorgangs_ids: [],
      }),
    });
    await readResponse(response);
    state.termineLoaded = false;
    await Promise.all([loadOverview(), loadTermine()]);
    if (elements.dialog.open) {
      elements.dialog.close();
    }
    activateTab("termine");
  } catch (error) {
    submit.disabled = false;
    status.className = "save-state is-error";
    status.textContent = "Erstellen fehlgeschlagen";
    showError(error.message);
  }
}

function openMailVorgangReviewDialog(
  entryId,
  analysis,
  suggestionsPayload = null,
  candidatesPayload = null,
) {
  const detail = state.selectedMailDetail;
  if (!detail || (detail.id !== entryId && detail.inboxId !== entryId)) {
    showError("Maildetails konnten fuer die Vorgangspruefung nicht geladen werden.");
    return;
  }
  elements.dialog.classList.add("is-vorgang");
  elements.dialog.classList.remove("has-rule-workspace");
  delete elements.dialog.dataset.vorgangId;
  delete elements.dialog.dataset.vorgangTransactionCount;
  elements.detailEyebrow.textContent = "Vorgang aus Mail";
  elements.detailTitle.textContent = analysis?.vorgang?.title || "Vorgang prüfen";
  elements.detailSubtitle.textContent =
    "Vorschlag prüfen, verknüpfen und importieren";
  elements.detailContent.replaceChildren(
    renderMailVorgangReview(
      detail,
      analysis,
      suggestionsPayload,
      entryId,
      candidatesPayload,
    ),
  );
  if (!elements.dialog.open) {
    elements.dialog.showModal();
  }
  applyMailZoom();
}

function renderMailVorgangReview(
  detail,
  analysis,
  suggestionsPayload = null,
  entryId = detail.id,
  candidatesPayload = null,
) {
  const section = mailElement("section", "mail-vorgang-review");
  section.append(
    mailElement("p", "eyebrow", "KI-Vorschlag"),
    mailElement("h4", "", "Vorgang, Dokumente, To-Dos und Termine prüfen"),
  );
  const form = mailElement("form", "mail-vorgang-review-form");
  form.dataset.mailVorgangReview = entryId;

  const layout = mailElement("div", "mail-vorgang-review-layout");
  const preview = mailElement("div", "mail-vorgang-document-preview");
  const previewHeading = mailElement("div", "mail-attachment-heading");
  previewHeading.append(mailElement("h4", "", "Dokument"));
  const zoom = mailElement("div", "mail-zoom-controls");
  const zoomOut = mailElement("button", "", "−");
  zoomOut.type = "button";
  zoomOut.dataset.mailZoomDelta = "-0.25";
  zoomOut.addEventListener("click", () => setMailZoom(state.mailZoom - 0.25));
  const range = document.createElement("input");
  range.type = "range";
  range.min = "25";
  range.max = "800";
  range.step = "25";
  range.value = String(Math.round(state.mailZoom * 100));
  range.dataset.mailZoomRange = "";
  range.addEventListener("input", () => setMailZoom(Number(range.value) / 100));
  const zoomIn = mailElement("button", "", "+");
  zoomIn.type = "button";
  zoomIn.dataset.mailZoomDelta = "0.25";
  zoomIn.addEventListener("click", () => setMailZoom(state.mailZoom + 0.25));
  const zoomValue = mailElement(
    "button",
    "mail-zoom-value",
    `${Math.round(state.mailZoom * 100)}%`,
  );
  zoomValue.type = "button";
  zoomValue.dataset.mailZoomReset = "";
  zoomValue.addEventListener("click", () => setMailZoom(1));
  zoom.append(zoomOut, range, zoomIn, zoomValue);
  previewHeading.append(zoom);
  const previewFrame = mailElement("div", "mail-attachment-preview");
  previewFrame.dataset.mailReviewAttachmentPreview = "";
  renderSelectedMailAttachment(previewFrame, {...detail, id: entryId});
  preview.append(previewHeading, previewFrame);

  const fields = mailElement("div", "mail-vorgang-review-fields");
  const reviewDocuments = mailReviewDocuments(detail, analysis.documents || []);
  fields.append(createMailReviewVorgangFields(analysis.vorgang || {}));
  fields.append(
    createMailReviewEntityList(
      "Dokumente",
      "document",
      reviewDocuments,
      createDocumentReviewRow,
    ),
    createMailReviewEntityList(
      "To-Dos",
      "todo",
      analysis.todos || [],
      createTodoReviewRow,
    ),
    createMailReviewEntityList(
      "Termine",
      "termin",
      analysis.termine || [],
      createTerminReviewRow,
    ),
  );
  const links = sourceLinkPayload({type: "mail", id: entryId});
  const transactionCandidates = {
    suggestions: {},
    candidates: {
      transactions: candidatesPayload?.transactions || [],
    },
  };
  const transactionItems = linkItems(transactionCandidates, "transactions");
  const transactionSection = createSuggestionSection(
    "Transaktionen verknüpfen",
    "transaction_ids",
    links.transaction_ids,
    transactionItems,
  );
  const classificationSection = createMailTransactionClassificationSection(
    form,
    transactionItems,
  );
  transactionSection.addEventListener("change", (event) => {
    if (event.target?.matches('input[type="checkbox"]')) {
      renderMailTransactionClassificationRows(
        classificationSection,
        form,
        transactionItems,
      );
    }
  });
  fields.append(
    transactionSection,
    classificationSection,
    createSuggestionSection(
      "Weitere Mails verknüpfen",
      "mail_ids",
      links.mail_ids,
      linkItems(suggestionsPayload, "mails"),
    ),
    createSuggestionSection(
      "Bestehende To-Dos verknüpfen",
      "todo_ids",
      links.todo_ids,
      linkItems(suggestionsPayload, "todos"),
      "todo",
    ),
    createSuggestionSection(
      "Bestehende Dokumente verknüpfen",
      "beleg_ids",
      links.beleg_ids,
      linkItems(suggestionsPayload, "belege"),
    ),
    createSuggestionSection(
      "Bestehende Termine verknüpfen",
      "termin_ids",
      links.termin_ids,
      linkItems(suggestionsPayload, "termine"),
      "termin",
    ),
  );
  layout.append(preview, fields);

  const topActions = createMailVorgangImportActions(true);
  const actions = createMailVorgangImportActions(false);
  form.append(topActions, layout, actions);
  updateMailVorgangImportActions(form);
  form.addEventListener("click", handleMailVorgangReviewClick);
  form.addEventListener("submit", submitMailVorgangImport);
  section.append(form);
  return section;
}

function createMailVorgangImportActions(isTop = false) {
  const actions = mailElement(
    "div",
    [
      "vorgang-form-actions",
      "mail-vorgang-import-actions",
      isTop ? "is-top" : "",
    ].filter(Boolean).join(" "),
  );
  const submit = mailElement("button", "primary-action");
  submit.type = "submit";
  submit.dataset.mailVorgangImportSubmit = "";
  const cancel = mailElement("button", "secondary-action", "Verwerfen");
  cancel.type = "button";
  cancel.addEventListener("click", () => {
    state.mailVorgangReview = null;
    if (elements.dialog.open) {
      elements.dialog.close();
    }
    renderMailDetail();
  });
  const status = mailElement("span", "save-state");
  status.dataset.mailVorgangImportStatus = "";
  actions.append(submit, cancel, status);
  return actions;
}

function mailVorgangImportSubmitLabel(form) {
  return form.elements.vorgang_completed?.checked
    ? "Vorgang abschließen"
    : "Vorgang anlegen";
}

function updateMailVorgangImportActions(form) {
  const label = mailVorgangImportSubmitLabel(form);
  for (const submit of form.querySelectorAll("[data-mail-vorgang-import-submit]")) {
    submit.textContent = label;
  }
}

function createMailReviewVorgangFields(vorgang) {
  const section = mailElement("section", "detail-section");
  section.append(mailElement("h3", "", "Vorgang"));
  const grid = mailElement("div", "detail-grid");
  grid.append(
    formTextField("Titel", "vorgang_title", vorgang.title || "", true),
    formVorgangTypeField("vorgang_type", vorgang.vorgangstyp || ""),
    formTextField(
      "Beschreibung",
      "vorgang_description",
      vorgang.description || "",
      false,
      true,
    ),
  );
  const completed = mailElement("label", "checkbox-field is-wide");
  const completedInput = document.createElement("input");
  completedInput.type = "checkbox";
  completedInput.name = "vorgang_completed";
  const completedText = mailElement("span");
  completedText.append(
    mailElement("strong", "", "Direkt abschließen"),
    mailElement(
      "small",
      "",
      "Nur möglich, wenn Transaktion, Dokument und Abschlussregeln passen.",
    ),
  );
  completed.append(completedInput, completedText);
  grid.append(completed);
  section.append(grid);
  return section;
}

function createMailTransactionClassificationSection(form, transactionItems) {
  const section = mailElement(
    "section",
    "detail-section mail-transaction-classifications",
  );
  section.dataset.mailTransactionClassifications = "";
  section.append(mailElement("h3", "", "Klassifikation verknüpfter Transaktionen"));
  renderMailTransactionClassificationRows(section, form, transactionItems);
  return section;
}

function renderMailTransactionClassificationRows(section, form, transactionItems) {
  section
    .querySelectorAll("[data-mail-transaction-classification-list]")
    .forEach((element) => element.remove());
  const list = mailElement("div", "mail-review-list");
  list.dataset.mailTransactionClassificationList = "";
  const selected = new Set(readSuggestionFields(form).transaction_ids || []);
  const itemsById = new Map(
    (transactionItems || [])
      .filter((item) => item?.id)
      .map((item) => [String(item.id), item]),
  );
  const selectedItems = [...selected].map((id) => ({
    ...(itemsById.get(id) || {}),
    id,
  }));
  if (!selectedItems.length) {
    list.append(
      mailElement(
        "p",
        "suggestion-empty",
        "Keine Transaktion ausgewählt.",
      ),
    );
  }
  for (const item of selectedItems) {
    list.append(createMailTransactionClassificationRow(item));
  }
  section.append(list);
}

function createMailTransactionClassificationRow(item) {
  const row = mailElement("fieldset", "mail-review-row classification-form");
  row.dataset.mailTransactionClassification = String(item.id || "");
  const legend = mailElement("legend");
  legend.append(
    mailElement("span", "", item.label || item.id),
    mailElement(
      "small",
      "",
      [
        item.date ? formatDateTimeOrDate(item.date) : "",
        item.amount ? currencyFormatter.format(Number(item.amount)) : "",
        item.sender,
        item.preview,
        item.status,
      ].filter(Boolean).join(" · "),
    ),
  );
  const classification = item.classification || {};
  row.append(
    legend,
    classificationField(
      "Transaktionstyp",
      "transaktionstyp",
      classification.transaktionstyp,
    ),
    classificationField(
      "Oberkategorie",
      "oberkategorie",
      classification.oberkategorie,
    ),
    classificationField(
      "Unterkategorie",
      "unterkategorie",
      classification.unterkategorie,
    ),
    classificationField("Sphäre", "sphaere", classification.sphaere),
    classificationField(
      "Fachliche Beschreibung",
      "fachliche_beschreibung",
      classification.fachliche_beschreibung,
      true,
      true,
    ),
  );
  configureClassificationEditorFields(row);
  return row;
}

function createMailReviewEntityList(title, type, items, rowFactory) {
  const section = mailElement("section", "detail-section mail-review-entities");
  section.append(mailElement("h3", "", title));
  const list = mailElement("div", "mail-review-list");
  list.dataset.reviewList = type;
  if (!items.length && type !== "todo") {
    list.append(mailElement("p", "suggestion-empty", "Keine Vorschläge."));
  }
  items.forEach((item, index) => {
    list.append(rowFactory(item, index, type));
  });
  if (type === "todo") {
    if (!items.length) {
      list.append(mailElement("p", "suggestion-empty", "Keine To-Do-Vorschläge."));
      list.append(rowFactory({}, 0, type));
    }
    const actions = mailElement("div", "mail-review-list-actions");
    const addButton = mailElement("button", "secondary-action", "To-Do hinzufügen");
    addButton.type = "button";
    addButton.dataset.addReviewTodo = "";
    addButton.addEventListener("click", () => {
      const nextIndex = list.querySelectorAll('[data-review-type="todo"]').length;
      list.append(rowFactory({}, nextIndex, type));
    });
    actions.append(addButton);
    section.append(list, actions);
    return section;
  }
  section.append(list);
  return section;
}

function mailReviewDocuments(detail, documents) {
  const byAttachmentIndex = new Map();
  for (const document of documents || []) {
    const attachmentIndex = Number(document?.attachment_index || 0);
    if (attachmentIndex > 0 && !byAttachmentIndex.has(attachmentIndex)) {
      byAttachmentIndex.set(attachmentIndex, document);
    }
  }
  const attachments = Array.isArray(detail?.attachments) ? detail.attachments : [];
  const result = [];
  const used = new Set();
  attachments.forEach((attachment, index) => {
    if (!attachment || typeof attachment !== "object") {
      return;
    }
    const attachmentIndex = Number(attachment.attachmentIndex || index + 1);
    if (attachmentIndex <= 0) {
      return;
    }
    const document = byAttachmentIndex.get(attachmentIndex) || {};
    used.add(attachmentIndex);
    result.push({
      enabled: document.enabled !== false,
      attachment_index: attachmentIndex,
      category: document.category || "sonstige_dokumente",
      filename: document.filename || attachment.filename || `anhang-${attachmentIndex}`,
      document_date: document.document_date || "",
      amount: document.amount || "",
      issuer: document.issuer || "",
      recipient: document.recipient || "",
      description: document.description || attachment.text || attachment.filename || "",
    });
  });
  for (const [attachmentIndex, document] of byAttachmentIndex) {
    if (!used.has(attachmentIndex)) {
      result.push({...document, attachment_index: attachmentIndex});
    }
  }
  return result;
}

function handleMailVorgangReviewClick(event) {
  const button = event.target.closest("[data-mail-review-attachment]");
  if (!button) {
    return;
  }
  state.selectedMailAttachment = Number(button.dataset.mailReviewAttachment);
  state.mailZoom = 1;
  const form = button.closest("[data-mail-vorgang-review]");
  const preview = form?.querySelector("[data-mail-review-attachment-preview]");
  if (preview) {
    renderSelectedMailAttachment(preview, {
      ...state.selectedMailDetail,
      id: form.dataset.mailVorgangReview,
    });
    applyMailZoom();
  }
}

function createReviewRow(type, index, title, enabledValue = true) {
  const row = mailElement("fieldset", "mail-review-row");
  row.dataset.reviewType = type;
  row.dataset.reviewIndex = String(index);
  const legend = mailElement("legend");
  const enabled = document.createElement("input");
  enabled.type = "checkbox";
  enabled.name = "enabled";
  enabled.checked = enabledValue !== false;
  legend.append(enabled, mailElement("span", "", title));
  row.append(legend);
  return row;
}

function createDocumentReviewRow(item, index) {
  const attachmentIndex = Number(item.attachment_index || 0);
  const title = attachmentIndex > 0
    ? `Anhang ${attachmentIndex}: ${item.filename || "Dokument"}`
    : item.filename || "Dokument";
  const row = createReviewRow("document", index, title, item.enabled);
  row.dataset.attachmentIndex = String(item.attachment_index || "");
  if (attachmentIndex > 0) {
    const previewButton = mailElement("button", "secondary-action", "Vorschau");
    previewButton.type = "button";
    previewButton.dataset.mailReviewAttachment = String(attachmentIndex);
    row.querySelector("legend").append(previewButton);
  }
  row.append(
    selectField("Kategorie", "category", {
      rechnungen: "Rechnungen",
      spendenbescheinigungen: "Spendenbescheinigungen",
      sonstige_dokumente: "Sonstige Dokumente",
    }, item.category || "sonstige_dokumente"),
    compactInputField("Dateiname", "filename", item.filename || ""),
    compactInputField("Dokumentdatum", "document_date", item.document_date || "", "date"),
    compactInputField("Betrag", "amount", item.amount || ""),
    compactInputField("Aussteller", "issuer", item.issuer || ""),
    compactInputField("Empfänger", "recipient", item.recipient || ""),
    compactTextareaField("Beschreibung", "description", item.description || ""),
  );
  return row;
}

function createTodoReviewRow(item, index) {
  const row = createReviewRow("todo", index, item.title || "To-Do");
  row.append(
    compactInputField("Titel", "title", item.title || ""),
    compactTextareaField("Beschreibung", "description", item.description || ""),
    compactInputField("Fällig am", "due_date", item.due_date || "", "date"),
    selectField("Priorität", "priority", {
      niedrig: "Niedrig",
      normal: "Normal",
      hoch: "Hoch",
    }, item.priority || "normal"),
  );
  return row;
}

function createTerminReviewRow(item, index) {
  const row = createReviewRow("termin", index, item.title || "Termin");
  row.append(
    compactInputField("Titel", "title", item.title || ""),
    compactTextareaField("Beschreibung", "description", item.description || ""),
    compactInputField(
      "Beginn",
      "starts_at",
      apiDateTimeToLocalInput(item.starts_at || ""),
      "datetime-local",
    ),
    compactInputField(
      "Ende",
      "ends_at",
      apiDateTimeToLocalInput(item.ends_at || ""),
      "datetime-local",
    ),
    compactInputField("Ort", "location", item.location || ""),
  );
  return row;
}

function compactInputField(labelText, name, value = "", type = "text") {
  const label = mailElement("label");
  label.append(mailElement("span", "detail-label", labelText));
  const input = document.createElement("input");
  input.name = name;
  input.type = type;
  input.value = value || "";
  label.append(input);
  return label;
}

function compactTextareaField(labelText, name, value = "") {
  const label = mailElement("label", "is-wide");
  label.append(mailElement("span", "detail-label", labelText));
  const textarea = document.createElement("textarea");
  textarea.name = name;
  textarea.rows = 2;
  textarea.value = value || "";
  label.append(textarea);
  return label;
}

function selectField(labelText, name, options, value = "") {
  const label = mailElement("label");
  label.append(mailElement("span", "detail-label", labelText));
  const select = document.createElement("select");
  select.name = name;
  for (const [optionValue, optionLabel] of Object.entries(options)) {
    const option = document.createElement("option");
    option.value = optionValue;
    option.textContent = optionLabel;
    select.append(option);
  }
  select.value = value;
  label.append(select);
  return label;
}

function handleMailDetailSubmit(event) {
  if (event.target.closest("[data-mail-vorgang-review]")) {
    submitMailVorgangImport(event);
    return;
  }
  if (event.target.closest("[data-link-mail-vorgang]")) {
    submitMailVorgangLink(event);
    return;
  }
  submitMailReply(event);
}

async function submitMailVorgangLink(event) {
  const form = event.target.closest("[data-link-mail-vorgang]");
  if (!form) {
    return;
  }
  event.preventDefault();
  const selected = form.querySelector('input[name="vorgangs_id"]:checked');
  const vorgangsId = selected?.value || "";
  const submit = form.querySelector("button[type='submit']");
  const status = form.querySelector(".save-state");
  await submitVorgangAssignment({
    form,
    submit,
    status,
    selectedId: vorgangsId,
    request: async () => {
      const response = await fetch(
      `/api/mail/${encodeURIComponent(form.dataset.linkMailVorgang)}/vorgaenge`,
      {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({vorgangs_id: vorgangsId}),
      },
      );
      const payload = await readResponse(response);
      updateSelectedMailVorgaenge(payload);
      state.vorgaengeLoaded = false;
    },
    onSaved: async () => {
      await loadOverview();
      renderMailDetail();
      const refreshedStatus = elements.mailDetail.querySelector(
        "[data-link-mail-vorgang] .save-state",
      );
      setAssignmentStatus(refreshedStatus, "saved", "Zuordnung gespeichert");
    },
  });
}

function setAssignmentStatus(status, stateName, message) {
  if (!status) return;
  status.className = `save-state is-${stateName}`;
  status.textContent = message;
}

async function submitVorgangAssignment({
  form, submit, status, selectedId, request, onSaved,
}) {
  if (!selectedId) {
    setAssignmentStatus(status, "error", "Bitte zuerst einen Vorgang auswählen.");
    return false;
  }
  if (form.dataset.assignmentSaving === "true") return false;
  form.dataset.assignmentSaving = "true";
  submit.disabled = true;
  setAssignmentStatus(status, "saving", "Zuordnung wird gespeichert");
  try {
    await request();
    setAssignmentStatus(status, "saved", "Zuordnung gespeichert");
    await onSaved();
    return true;
  } catch (error) {
    delete form.dataset.assignmentSaving;
    submit.disabled = false;
    setAssignmentStatus(status, "error", `Zuordnung fehlgeschlagen: ${error.message}`);
    return false;
  }
}

async function submitMailVorgangImport(event) {
  const form = event.target.closest("[data-mail-vorgang-review]");
  if (!form) {
    return;
  }
  event.preventDefault();
  const submitButtons = form.querySelectorAll("[data-mail-vorgang-import-submit]");
  const statuses = form.querySelectorAll("[data-mail-vorgang-import-status]");
  for (const submit of submitButtons) {
    submit.disabled = true;
  }
  for (const status of statuses) {
    status.className = "save-state is-saving";
    status.textContent = "Import läuft";
  }
  try {
    const response = await fetch(
      `/api/mail/${encodeURIComponent(form.dataset.mailVorgangReview)}/vorgang-import`,
      {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(readMailVorgangReviewForm(form)),
      },
    );
    const payload = await readResponse(response);
    state.mailVorgangReview = null;
    rememberVorgangType(form.elements.vorgang_type.value);
    state.vorgaengeLoaded = false;
    state.todosLoaded = false;
    state.termineLoaded = false;
    await Promise.all([loadOverview(), loadVorgaenge()]);
    if (elements.dialog.open) {
      elements.dialog.close();
    }
    activateTab("vorgaenge");
    const completion = payload.direct_completion || {};
    const completed = completion.completed
      || payload.vorgang?.status === "abgeschlossen";
    const message = completion.rejected
      ? `Vorgang importiert, Abschluss abgewiesen: ${completion.message}`
      : completed
        ? "Vorgang importiert und abgeschlossen"
        : "Vorgang importiert";
    await loadVorgangWorkspace(
      payload.vorgang.vorgangs_id,
      message,
    );
  } catch (error) {
    for (const submit of submitButtons) {
      submit.disabled = false;
    }
    for (const status of statuses) {
      status.className = "save-state is-error";
      status.textContent = "Import fehlgeschlagen";
    }
    showError(error.message);
  }
}

function readMailVorgangReviewForm(form) {
  const links = readSuggestionFields(form);
  return {
    vorgang: {
      title: form.elements.vorgang_title.value,
      description: form.elements.vorgang_description.value,
      vorgangstyp: form.elements.vorgang_type.value,
      completed: form.elements.vorgang_completed.checked,
    },
    links,
    transaction_classifications: readMailTransactionClassifications(
      form,
      links.transaction_ids || [],
    ),
    documents: readReviewRows(form, "document").map((entry) => ({
      enabled: entry.enabled,
      attachment_index: Number(entry.row.dataset.attachmentIndex),
      category: entry.values.category,
      filename: entry.values.filename,
      document_date: entry.values.document_date,
      amount: entry.values.amount,
      issuer: entry.values.issuer,
      recipient: entry.values.recipient,
      description: entry.values.description,
    })),
    todos: readReviewRows(form, "todo").map((entry) => ({
      enabled: entry.enabled,
      title: entry.values.title,
      description: entry.values.description,
      due_date: entry.values.due_date,
      priority: entry.values.priority,
    })),
    termine: readReviewRows(form, "termin").map((entry) => ({
      enabled: entry.enabled,
      title: entry.values.title,
      description: entry.values.description,
      starts_at: localDateTimeToApiValue(entry.values.starts_at),
      ends_at: localDateTimeToApiValue(entry.values.ends_at),
      location: entry.values.location,
    })),
  };
}

function readMailTransactionClassifications(form, transactionIds) {
  const selected = new Set(transactionIds || []);
  return [
    ...form.querySelectorAll("[data-mail-transaction-classification]"),
  ]
    .filter((row) => selected.has(row.dataset.mailTransactionClassification))
    .map((row) => ({
      transaction_id: row.dataset.mailTransactionClassification,
      ...Object.fromEntries(
        [...row.querySelectorAll("input, textarea, select")]
          .filter((field) => field.name)
          .map((field) => [field.name, field.value]),
      ),
    }));
}

function readReviewRows(form, type) {
  return [...form.querySelectorAll(`[data-review-type="${type}"]`)].map(
    (row) => {
      const values = {};
      for (const field of row.querySelectorAll("input, textarea, select")) {
        if (field.name && field.name !== "enabled") {
          values[field.name] = field.value;
        }
      }
      return {
        row,
        enabled: row.querySelector('input[name="enabled"]').checked,
        values,
      };
    },
  );
}

async function handleMailDetailClick(event) {
  const todoButton = event.target.closest("[data-create-todo-from-summary]");
  if (todoButton) {
    await createTodoFromMailSummary(todoButton);
    return;
  }
  const manualTodoButton = event.target.closest(
    "[data-create-manual-todo-from-summary]",
  );
  if (manualTodoButton) {
    openManualTodoFromMailSummary(manualTodoButton.dataset.createManualTodoFromSummary);
    return;
  }
  const openButton = event.target.closest("[data-open-mail]");
  if (openButton) {
    await loadMailDetail(openButton.dataset.openMail);
    return;
  }
  const summaryButton = event.target.closest("[data-summarize-mail]");
  if (summaryButton) {
    await toggleMailSummary(
      summaryButton.dataset.summarizeMail,
      summaryButton,
    );
    return;
  }
  const readButton = event.target.closest("[data-mark-mail-read]");
  if (readButton) {
    await markMailRead(readButton.dataset.markMailRead, readButton);
    return;
  }
  const tagButton = event.target.closest("[data-toggle-mail-tag]");
  if (tagButton) {
    await toggleMailTag(tagButton.dataset.toggleMailTag, tagButton);
    return;
  }
  const deleteButton = event.target.closest("[data-delete-mail]");
  if (deleteButton) {
    await deleteMail(deleteButton.dataset.deleteMail, deleteButton);
    return;
  }
  const unlinkVorgangButton = event.target.closest("[data-unlink-mail-vorgang]");
  if (unlinkVorgangButton) {
    await unlinkMailVorgang(
      unlinkVorgangButton.dataset.unlinkMailVorgang,
      unlinkVorgangButton,
    );
    return;
  }
  const openVorgangButton = event.target.closest("[data-open-vorgang]");
  if (openVorgangButton) {
    await openVorgang(openVorgangButton.dataset.openVorgang);
    return;
  }
  const createVorgangButton = event.target.closest("[data-mail-create-vorgang]");
  if (createVorgangButton) {
    await startMailVorgangReview(
      createVorgangButton.dataset.mailCreateVorgang,
      createVorgangButton,
    );
    return;
  }
  const createTerminButton = event.target.closest("[data-mail-create-termin]");
  if (createTerminButton) {
    await startMailTerminSuggestion(
      createTerminButton.dataset.mailCreateTermin,
      createTerminButton,
    );
    return;
  }
  const attachmentButton = event.target.closest("[data-mail-attachment]");
  if (attachmentButton) {
    state.selectedMailAttachment = Number(
      attachmentButton.dataset.mailAttachment,
    );
    state.mailZoom = 1;
    renderMailDetail();
    return;
  }
  const zoomButton = event.target.closest("[data-mail-zoom-delta]");
  if (zoomButton) {
    setMailZoom(
      state.mailZoom + Number(zoomButton.dataset.mailZoomDelta),
    );
    return;
  }
  if (event.target.closest("[data-mail-zoom-reset]")) {
    setMailZoom(1);
  }
}

async function unlinkMailVorgang(vorgangsId, button) {
  const detail = state.selectedMailDetail;
  const entryId = detail?.id || detail?.inboxId || state.selectedMailId;
  if (!entryId || !vorgangsId) {
    return;
  }
  button.disabled = true;
  try {
    const response = await fetch(
      `/api/mail/${encodeURIComponent(entryId)}/vorgaenge/${encodeURIComponent(vorgangsId)}`,
      {method: "DELETE"},
    );
    const payload = await readResponse(response);
    updateSelectedMailVorgaenge(payload);
    state.vorgaengeLoaded = false;
    await loadOverview();
    renderMailDetail();
  } catch (error) {
    button.disabled = false;
    showError(error.message);
  }
}

function updateSelectedMailVorgaenge(payload) {
  if (!state.selectedMailDetail) {
    return;
  }
  state.selectedMailDetail = {
    ...state.selectedMailDetail,
    vorgangs_ids: payload.vorgangs_ids || [],
    vorgaenge: dedupeVorgaenge(payload.vorgaenge || []),
  };
}

function handleMailPreviewClick(event) {
  const attachmentButton = event.target.closest("[data-mail-attachment]");
  if (attachmentButton) {
    state.selectedMailAttachment = Number(
      attachmentButton.dataset.mailAttachment,
    );
    const preview = elements.entityPreviewContent.querySelector(
      "[data-mail-attachment-preview]",
    );
    const detailId = elements.entityPreviewContent.dataset.mailPreviewId;
    if (preview && detailId) {
      const attachmentPane = attachmentButton.closest(".mail-attachment-pane");
      const attachments = [...attachmentPane.querySelectorAll(
        "[data-mail-attachment]",
      )].map((button) => ({
        attachmentIndex: Number(button.dataset.mailAttachment),
      }));
      for (const button of attachmentPane.querySelectorAll(
        "[data-mail-attachment]",
      )) {
        button.classList.toggle(
          "is-selected",
          button === attachmentButton,
        );
      }
      const detail = {
        id: detailId,
        attachments: state.entityPreviewAttachments || attachments,
      };
      renderSelectedMailAttachment(preview, detail);
    }
    return;
  }
  const zoomButton = event.target.closest("[data-mail-zoom-delta]");
  if (zoomButton) {
    setMailZoom(
      state.mailZoom + Number(zoomButton.dataset.mailZoomDelta),
    );
    return;
  }
  if (event.target.closest("[data-mail-zoom-reset]")) {
    setMailZoom(1);
  }
}

function handleMailDetailInput(event) {
  const mailVorgangSearch = event.target.closest("[data-mail-vorgang-search]");
  if (mailVorgangSearch) {
    state.mailVorgangSearch = mailVorgangSearch.value.trim();
    clearTimeout(mailVorgangSearchTimer);
    mailVorgangSearchTimer = setTimeout(loadMailVorgangCandidates, 250);
    return;
  }
  const mailVorgangHideCompleted = event.target.closest(
    "[data-mail-vorgang-hide-completed]",
  );
  if (mailVorgangHideCompleted) {
    state.mailVorgangHideCompleted = mailVorgangHideCompleted.checked;
    clearTimeout(mailVorgangSearchTimer);
    mailVorgangSearchTimer = setTimeout(loadMailVorgangCandidates, 150);
    return;
  }
  if (event.target.matches('input[name="vorgang_completed"]')) {
    const form = event.target.closest("[data-mail-vorgang-review]");
    if (form) {
      updateMailVorgangImportActions(form);
    }
    return;
  }
  if (event.target.matches('input[name="vorgangs_id"]')) {
    const form = event.target.closest("[data-link-mail-vorgang]");
    if (form) {
      setMailVorgangSubmitState(form);
    }
    return;
  }
  if (event.target.matches("[data-mail-zoom-range]")) {
    setMailZoom(Number(event.target.value) / 100);
  }
}

function setMailZoom(value) {
  state.mailZoom = Math.min(8, Math.max(0.25, value));
  applyMailZoom();
}

function applyMailZoom() {
  for (const root of [
    elements.mailDetail,
    elements.detailContent,
    elements.entityPreviewContent,
  ]) {
    for (const content of root.querySelectorAll("[data-mail-preview-content]")) {
      content.style.width = `${state.mailZoom * 100}%`;
      const textPreview = content.querySelector("pre");
      if (textPreview) {
        textPreview.style.fontSize = `${0.78 * state.mailZoom}rem`;
      }
    }
    for (const range of root.querySelectorAll("[data-mail-zoom-range]")) {
      range.value = String(Math.round(state.mailZoom * 100));
    }
    for (const value of root.querySelectorAll("[data-mail-zoom-reset]")) {
      value.textContent = `${Math.round(state.mailZoom * 100)}%`;
    }
  }
}

async function toggleMailTag(entryId, button) {
  const mail = state.mails.find((item) => item.id === entryId);
  if (!mail) {
    return;
  }
  const nextTag = mail.tag === "BSV" ? "Privat" : "BSV";
  button.disabled = true;
  try {
    const response = await fetch(
      `/api/mail/${encodeURIComponent(entryId)}/tag`,
      {
        method: "PATCH",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({tag: nextTag}),
      },
    );
    const payload = await readResponse(response);
    const affectedIds = mailAffectedIds(payload, entryId);
    for (const item of state.mails) {
      if (affectedIds.has(item.id)) {
        item.tag = payload.tag;
      }
    }
    renderMailList();
    if (affectedIds.has(state.selectedMailId)) {
      renderMailDetail();
    }
  } catch (error) {
    button.disabled = false;
    showError(error.message);
  }
}

async function updateMailSpamThreshold() {
  const percent = Number(elements.mailSpamThreshold.value);
  if (!Number.isFinite(percent) || percent < 0 || percent > 100) {
    showError("Die Spam-Schwelle muss zwischen 0 und 100 Prozent liegen.");
    elements.mailSpamThreshold.value = String(
      Math.round(state.mailSpamThreshold * 100),
    );
    return;
  }
  elements.mailSpamThreshold.disabled = true;
  try {
    const response = await fetch("/api/mail/settings", {
      method: "PATCH",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({spam_threshold: percent / 100}),
    });
    const payload = await readResponse(response);
    state.mailSpamThreshold = Number(payload.spam_threshold);
    renderMailList();
    renderMailDetail();
  } catch (error) {
    elements.mailSpamThreshold.value = String(
      Math.round(state.mailSpamThreshold * 100),
    );
    showError(error.message);
  } finally {
    elements.mailSpamThreshold.disabled = false;
  }
}

async function deleteMail(entryId, button) {
  button.disabled = true;
  button.textContent = "Wird gelöscht";
  try {
    const response = await fetch(
      `/api/mail/${encodeURIComponent(entryId)}`,
      {method: "DELETE"},
    );
    const payload = await readResponse(response);
    const affectedIds = mailAffectedIds(payload, entryId);
    state.mails = state.mails.filter((mail) => !affectedIds.has(mail.id));
    for (const id of affectedIds) {
      state.mailDeleteSelections.delete(id);
    }
    elements.mailCount.textContent = String(state.mails.length);
    renderMailList();
    clearMailDetail(
      affectedIds.size > 1
        ? "Mailverlauf wurde gelöscht."
        : "Mail wurde gelöscht.",
    );
    loadOverview();
  } catch (error) {
    button.disabled = false;
    button.textContent = "Löschen";
    showError(error.message);
  }
}

async function deleteSelectedMails() {
  const entryIds = [...state.mailDeleteSelections];
  if (!entryIds.length) {
    updateMailDeleteSelectedButton();
    return;
  }
  elements.mailDeleteSelected.disabled = true;
  elements.mailDeleteSpam.disabled = true;
  elements.mailRefresh.disabled = true;
  elements.mailDeleteStatus.textContent =
    `${entryIds.length} markierte Mail(s) werden gelöscht`;
  try {
    const response = await fetch("/api/mail/delete-selected", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({entry_ids: entryIds}),
    });
    const payload = await readResponse(response);
    const deletedIds = new Set(payload.deleted || []);
    for (const entryId of deletedIds) {
      state.mailDeleteSelections.delete(entryId);
    }
    state.mails = state.mails.filter((mail) => !deletedIds.has(mail.id));
    elements.mailCount.textContent = String(state.mails.length);
    if (deletedIds.has(state.selectedMailId)) {
      clearMailDetail(
        deletedIds.size === 1
          ? "Markierte Mail wurde gelöscht."
          : `${deletedIds.size} markierte Mails wurden gelöscht.`,
      );
    } else {
      renderMailList();
      renderMailDetail();
    }
    elements.mailDeleteStatus.textContent = payload.failed_count
      ? `${payload.deleted_count} gelöscht, ${payload.failed_count} fehlgeschlagen`
      : payload.deleted_count === 1
        ? "1 markierte Mail gelöscht"
        : `${payload.deleted_count} markierte Mails gelöscht`;
    if (payload.failed_count) {
      showError(
        `${payload.failed_count} markierte Mail(s) konnten nicht gelöscht werden.`,
      );
    }
    loadOverview();
  } catch (error) {
    showError(error.message);
  } finally {
    elements.mailRefresh.disabled = false;
    updateMailDeleteSpamButton();
    updateMailDeleteSelectedButton();
  }
}

async function deleteSpamMails() {
  const candidates = mailDeleteCandidates();
  if (!candidates.length) {
    updateMailDeleteSpamButton();
    return;
  }
  elements.mailDeleteSpam.disabled = true;
  elements.mailRefresh.disabled = true;
  elements.mailSpamThreshold.disabled = true;
  elements.mailDeleteStatus.textContent =
    `${candidates.length} Spam-Mail(s) werden gelöscht`;
  const deletedIds = [];
  const failures = [];
  try {
    const deletedSet = new Set();
    for (const mail of candidates) {
      if (deletedSet.has(mail.id)) {
        continue;
      }
      try {
        const response = await fetch(
          `/api/mail/${encodeURIComponent(mail.id)}`,
          {method: "DELETE"},
        );
        const payload = await readResponse(response);
        for (const id of mailAffectedIds(payload, mail.id)) {
          deletedSet.add(id);
        }
      } catch (error) {
        failures.push({id: mail.id, message: error.message});
      }
    }
    deletedIds.push(...deletedSet);
    for (const entryId of deletedSet) {
      state.mailDeleteSelections.delete(entryId);
    }
    state.mails = state.mails.filter((mail) => !deletedSet.has(mail.id));
    elements.mailCount.textContent = String(state.mails.length);
    if (deletedSet.has(state.selectedMailId)) {
      clearMailDetail(
        deletedIds.length === 1
          ? "Spam-Mail wurde gelöscht."
          : `${deletedIds.length} Spam-Mails wurden gelöscht.`,
      );
    } else {
      renderMailList();
      renderMailDetail();
    }
    elements.mailDeleteStatus.textContent = failures.length
      ? `${deletedIds.length} gelöscht, ${failures.length} fehlgeschlagen`
      : deletedIds.length === 1
        ? "1 Spam-Mail gelöscht"
        : `${deletedIds.length} Spam-Mails gelöscht`;
    if (failures.length) {
      showError(
        `${failures.length} Spam-Mail(s) konnten nicht gelöscht werden.`,
      );
    }
    loadOverview();
  } finally {
    elements.mailRefresh.disabled = false;
    elements.mailSpamThreshold.disabled = false;
    updateMailDeleteSpamButton();
  }
}

async function submitMailReply(event) {
  const form = event.target.closest("[data-mail-reply-form]");
  if (!form) {
    return;
  }
  event.preventDefault();
  const formData = new FormData(form);
  const body = formData.get("body")?.toString() || "";
  const toRecipients = parseReplyRecipients(
    formData.get("to_recipients")?.toString() || "",
  );
  const button = form.querySelector("button[type='submit']");
  const status = form.querySelector(".mail-reply-status");
  button.disabled = true;
  status.textContent = "Antwort wird gesendet";
  try {
    const response = await fetch(
      `/api/mail/${encodeURIComponent(form.dataset.mailReplyForm)}/reply`,
      {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({body, to_recipients: toRecipients}),
      },
    );
    await readResponse(response);
    form.reset();
    status.textContent = "Antwort wurde gesendet.";
  } catch (error) {
    status.textContent = "Senden fehlgeschlagen";
    showError(error.message);
  } finally {
    button.disabled = false;
  }
}

function parseReplyRecipients(value) {
  return String(value || "")
    .split(/[;,\n]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function mailAffectedIds(payload, fallbackId) {
  const rawIds = payload.affected_ids || payload.deleted || [fallbackId];
  return new Set(
    rawIds
      .map((value) => String(value || "").trim())
      .filter(Boolean),
  );
}

function clearMailDetail(message = "") {
  state.selectedMailId = null;
  state.selectedMailDetail = null;
  state.selectedMailAttachment = null;
  elements.mailDetail.replaceChildren();
  const empty = mailElement("div", "mail-detail-empty");
  empty.append(
    mailElement("strong", "", message || "Mail auswählen"),
    mailElement(
      "p",
      "",
      message
        ? ""
        : "Mailtext und Anhänge werden anschließend nebeneinander angezeigt.",
    ),
  );
  elements.mailDetail.append(empty);
  renderMailList();
}

function mailElement(tagName, className = "", text = "") {
  const element = document.createElement(tagName);
  if (className) {
    element.className = className;
  }
  if (text !== "") {
    element.textContent = text;
  }
  return element;
}

function formatFileSize(value) {
  const bytes = Number(value);
  if (!Number.isFinite(bytes) || bytes < 0) {
    return "";
  }
  if (bytes < 1000) {
    return `${bytes} B`;
  }
  if (bytes < 1_000_000) {
    return `${(bytes / 1000).toFixed(1)} KB`;
  }
  return `${(bytes / 1_000_000).toFixed(1)} MB`;
}

async function loadBalanceHistory() {
  if (!elements.historyDateFrom.value || !elements.historyDateTo.value) {
    return;
  }
  if (elements.historyDateFrom.value > elements.historyDateTo.value) {
    showError("Das Von-Datum darf nicht nach dem Bis-Datum liegen.");
    return;
  }
  elements.historyLoading.hidden = false;
  elements.historyEmpty.hidden = true;
  const parameters = new URLSearchParams({
    date_from: elements.historyDateFrom.value,
    date_to: elements.historyDateTo.value,
  });
  try {
    const response = await fetch(`/api/balance-history?${parameters}`);
    state.balanceHistory = await readResponse(response);
    renderHistorySeriesSelector(state.balanceHistory.series);
    renderBalanceHistoryChart();
  } catch (error) {
    showError(error.message);
    state.balanceHistory = null;
    elements.balanceHistoryChart.replaceChildren();
    elements.historyEmpty.hidden = false;
  } finally {
    elements.historyLoading.hidden = true;
  }
}

function renderHistorySeriesSelector(series) {
  const validIds = new Set(series.map((item) => item.id));
  for (const selected of [...state.selectedHistorySeries]) {
    if (!validIds.has(selected)) {
      state.selectedHistorySeries.delete(selected);
    }
  }
  elements.historySeriesSelector.replaceChildren();
  series.forEach((item, index) => {
    const label = document.createElement("label");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = state.selectedHistorySeries.has(item.id);
    checkbox.addEventListener("change", () => {
      if (checkbox.checked) {
        state.selectedHistorySeries.add(item.id);
      } else {
        state.selectedHistorySeries.delete(item.id);
      }
      renderBalanceHistoryChart();
    });
    const color = document.createElement("span");
    color.className = "series-color";
    color.style.backgroundColor = chartColors[index % chartColors.length];
    const text = document.createElement("span");
    text.textContent = item.label;
    label.append(checkbox, color, text);
    elements.historySeriesSelector.append(label);
  });
}

function renderBalanceHistoryChart() {
  const svg = elements.balanceHistoryChart;
  svg.replaceChildren();
  if (!state.balanceHistory) {
    elements.historyEmpty.hidden = false;
    return;
  }
  const selected = state.balanceHistory.series.filter((series) =>
    state.selectedHistorySeries.has(series.id),
  );
  const points = selected.flatMap((series) =>
    series.values
      .filter((point) => point.value !== null)
      .map((point) => ({
        date: new Date(`${point.date}T00:00:00`).getTime(),
        value: Number(point.value),
      })),
  );
  if (!selected.length || !points.length) {
    elements.historyEmpty.hidden = false;
    return;
  }
  elements.historyEmpty.hidden = true;

  const width = 1000;
  const height = 360;
  const margin = {top: 24, right: 34, bottom: 48, left: 82};
  const plotWidth = width - margin.left - margin.right;
  const plotHeight = height - margin.top - margin.bottom;
  const minDate = Math.min(...points.map((point) => point.date));
  const maxDate = Math.max(...points.map((point) => point.date));
  const axis = calculateNiceAxis(
    Math.min(...points.map((point) => point.value)),
    Math.max(...points.map((point) => point.value)),
  );
  const minValue = axis.min;
  const maxValue = axis.max;

  const x = (value) =>
    margin.left +
    ((value - minDate) / Math.max(maxDate - minDate, 1)) * plotWidth;
  const y = (value) =>
    margin.top +
    ((maxValue - value) / Math.max(maxValue - minValue, 1)) * plotHeight;

  for (const value of [...axis.ticks].reverse()) {
    const yPosition = y(value);
    appendSvgLine(
      svg,
      margin.left,
      yPosition,
      width - margin.right,
      yPosition,
      value === 0 ? "chart-grid is-zero" : "chart-grid",
    );
    appendSvgText(
      svg,
      margin.left - 12,
      yPosition + 4,
      formatAxisCurrency(value, axis.step),
      "end",
    );
  }
  for (let index = 0; index <= 4; index += 1) {
    const ratio = index / 4;
    const timestamp = minDate + ratio * (maxDate - minDate);
    const xPosition = margin.left + ratio * plotWidth;
    appendSvgText(
      svg,
      xPosition,
      height - 18,
      formatChartDate(new Date(timestamp)),
      "middle",
    );
  }

  selected.forEach((series) => {
    const seriesIndex = state.balanceHistory.series.findIndex(
      (item) => item.id === series.id,
    );
    const color = chartColors[seriesIndex % chartColors.length];
    let path = "";
    let drawing = false;
    for (const point of series.values) {
      if (point.value === null) {
        drawing = false;
        continue;
      }
      const xPosition = x(new Date(`${point.date}T00:00:00`).getTime());
      const yPosition = y(Number(point.value));
      path += `${drawing ? " L" : " M"} ${xPosition} ${yPosition}`;
      drawing = true;
    }
    const pathElement = document.createElementNS(
      "http://www.w3.org/2000/svg",
      "path",
    );
    pathElement.setAttribute("d", path.trim());
    pathElement.setAttribute(
      "class",
      `chart-line${series.is_total ? " is-total" : ""}`,
    );
    pathElement.setAttribute("stroke", color);
    svg.append(pathElement);

    const lastPoint = [...series.values]
      .reverse()
      .find((point) => point.value !== null);
    if (lastPoint) {
      const circle = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "circle",
      );
      circle.setAttribute(
        "cx",
        x(new Date(`${lastPoint.date}T00:00:00`).getTime()),
      );
      circle.setAttribute("cy", y(Number(lastPoint.value)));
      circle.setAttribute("r", series.is_total ? "5" : "4");
      circle.setAttribute("fill", color);
      circle.setAttribute("class", "chart-point");
      const title = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "title",
      );
      title.textContent =
        `${series.label}: ${currencyFormatter.format(Number(lastPoint.value))}`;
      circle.append(title);
      svg.append(circle);
    }
  });
}

function calculateNiceAxis(dataMin, dataMax, targetTicks = 10) {
  let min = dataMin;
  let max = dataMax;
  if (min === max) {
    const expansion = Math.max(Math.abs(min) * 0.1, 1);
    min -= expansion;
    max += expansion;
  } else {
    const padding = (max - min) * 0.03;
    min -= padding;
    max += padding;
  }

  const rawStep = (max - min) / Math.max(targetTicks - 1, 1);
  const baseExponent = Math.floor(Math.log10(rawStep));
  let best = null;
  for (
    let exponent = baseExponent - 1;
    exponent <= baseExponent + 1;
    exponent += 1
  ) {
    const magnitude = 10 ** exponent;
    for (const multiplier of [1, 2, 5, 10]) {
      const step = multiplier * magnitude;
      const axisMin = Math.floor(min / step) * step;
      const axisMax = Math.ceil(max / step) * step;
      const count = Math.round((axisMax - axisMin) / step) + 1;
      if (count < 2 || count > 20) {
        continue;
      }
      const score =
        Math.abs(count - targetTicks) +
        (count < 6 || count > 14 ? 4 : 0);
      if (!best || score < best.score || (
        score === best.score && count > best.count
      )) {
        best = {min: axisMin, max: axisMax, step, count, score};
      }
    }
  }
  const selected = best || {
    min,
    max,
    step: rawStep,
    count: targetTicks,
  };
  const ticks = Array.from(
    {length: selected.count},
    (_, index) => Number(
      (selected.min + index * selected.step).toPrecision(12),
    ),
  );
  return {...selected, ticks};
}

function formatAxisCurrency(value, step) {
  return new Intl.NumberFormat("de-DE", {
    style: "currency",
    currency: "EUR",
    minimumFractionDigits: 0,
    maximumFractionDigits: step < 1 ? 2 : 0,
  }).format(value);
}

function appendSvgLine(svg, x1, y1, x2, y2, className = "chart-grid") {
  const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
  line.setAttribute("x1", x1);
  line.setAttribute("y1", y1);
  line.setAttribute("x2", x2);
  line.setAttribute("y2", y2);
  line.setAttribute("class", className);
  svg.append(line);
}

function appendSvgText(svg, x, y, value, anchor) {
  const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
  text.setAttribute("x", x);
  text.setAttribute("y", y);
  text.setAttribute("text-anchor", anchor);
  text.setAttribute("class", "chart-axis-label");
  text.textContent = value;
  svg.append(text);
}

async function loadRules() {
  elements.ruleFormStatus.textContent = "Regeln werden geladen";
  elements.completionRuleFormStatus.textContent =
    "Abschlussregeln werden geladen";
  try {
    const parameters = new URLSearchParams({search: state.ruleSearch});
    const completionParameters = new URLSearchParams({
      search: state.completionRuleSearch,
    });
    const [
      rulesResponse,
      completionRulesResponse,
      optionsResponse,
    ] = await Promise.all([
      fetch(`/api/rules?${parameters}`),
      fetch(`/api/completion-rules?${completionParameters}`),
      fetch("/api/classification-options"),
    ]);
    const [payload, completionPayload, options] = await Promise.all([
      readResponse(rulesResponse),
      readResponse(completionRulesResponse),
      readResponse(optionsResponse),
    ]);
    state.classificationOptions = options;
    renderRules(payload);
    renderCompletionRules(completionPayload);
    state.rulesLoaded = true;
    elements.ruleFormStatus.textContent = "";
    elements.completionRuleFormStatus.textContent = "";
  } catch (error) {
    elements.ruleFormStatus.textContent = "Regeln konnten nicht geladen werden";
    elements.completionRuleFormStatus.textContent =
      "Abschlussregeln konnten nicht geladen werden";
    showError(error.message);
  }
}

function renderRules(payload) {
  state.ruleMatchFields = payload.match_fields;
  state.ruleMatchOperators = payload.match_operators;
  state.ruleLogicConnectors = payload.logic_connectors;
  elements.ruleCount.textContent =
    `${integerFormatter.format(payload.rules.length)} ` +
    `${payload.rules.length === 1 ? "Regel" : "Regeln"}`;
  renderRuleCards(
    elements.ruleList,
    payload.rules,
    editRule,
    deleteRule,
  );
  if (!elements.ruleConditions.children.length) {
    addRuleCondition();
  }
  configureRuleClassificationFields(elements.ruleForm);
}

function renderCompletionRules(payload) {
  state.completionRuleMatchFields = payload.match_fields;
  state.ruleMatchOperators = payload.match_operators;
  state.ruleLogicConnectors = payload.logic_connectors;
  elements.completionRuleCount.textContent =
    `${integerFormatter.format(payload.rules.length)} ` +
    `${payload.rules.length === 1 ? "Regel" : "Regeln"}`;
  renderRuleCards(
    elements.completionRuleList,
    payload.rules,
    editCompletionRule,
    deleteCompletionRule,
    () => "Vorgang automatisch abschließen",
    state.completionRuleMatchFields,
  );
  if (!elements.completionRuleConditions.children.length) {
    addRuleCondition(
      {},
      elements.completionRuleConditions,
      elements.completionRuleAddCondition,
      state.completionRuleMatchFields,
    );
  }
}

function renderRuleCards(
  container,
  rules,
  onEdit,
  onDelete,
  resultFormatter = (rule) =>
    `${rule.transaction_type} · ${rule.top_category} · ` +
    `${rule.sub_category} · ${rule.sphere}`,
  matchFields = state.ruleMatchFields,
) {
  container.replaceChildren();
  for (const rule of rules) {
    const card = document.createElement("article");
    card.className = "rule-card";
    card.tabIndex = 0;
    card.setAttribute("role", "button");
    card.setAttribute("aria-label", `Regel ${rule.name} bearbeiten`);
    card.addEventListener("click", () => onEdit(rule));
    card.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        onEdit(rule);
      }
    });
    const header = document.createElement("div");
    header.className = "rule-card-header";
    const name = document.createElement("strong");
    name.textContent = rule.name;
    const status = document.createElement("span");
    status.className = `rule-state${rule.enabled ? "" : " is-disabled"}`;
    status.textContent = rule.enabled ? "Aktiv" : "Inaktiv";
    const remove = document.createElement("button");
    remove.className = "rule-delete";
    remove.type = "button";
    remove.textContent = "Entfernen";
    remove.setAttribute("aria-label", `Regel ${rule.name} entfernen`);
    remove.addEventListener("click", (event) => {
      event.stopPropagation();
      onDelete(rule);
    });
    remove.addEventListener("keydown", (event) => {
      event.stopPropagation();
    });
    const actions = document.createElement("div");
    actions.className = "rule-card-actions";
    actions.append(status, remove);
    const condition = document.createElement("p");
    condition.textContent = formatRuleConditions(rule, matchFields);
    const result = document.createElement("p");
    result.className = "rule-result";
    result.textContent = resultFormatter(rule);
    header.append(name, actions);
    card.append(header, condition, result);
    container.append(card);
  }
}

function formatRuleConditions(rule, matchFields = state.ruleMatchFields) {
  const conditions = rule.conditions?.length
    ? rule.conditions
    : [{
      connector: "",
      match_field: rule.match_field,
      match_operator: rule.match_operator,
      match_value: rule.match_value,
    }];
  return conditions.map((condition, index) => {
    const connector = index
      ? `${state.ruleLogicConnectors[condition.connector] ||
          condition.connector} `
      : "";
    const field =
      matchFields[condition.match_field] || condition.match_field;
    const operator =
      state.ruleMatchOperators[condition.match_operator] ||
      condition.match_operator;
    return `${connector}${field} ${operator} „${condition.match_value}“`;
  }).join(" ");
}

function fillSelect(select, options) {
  const current = select.value;
  select.replaceChildren();
  for (const [value, label] of Object.entries(options)) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    select.append(option);
  }
  if ([...select.options].some((option) => option.value === current)) {
    select.value = current;
  }
}

function configureRuleClassificationFields(form) {
  configureClassificationFields(form, {
    transactionType: "transaction_type",
    topCategory: "top_category",
    subCategory: "sub_category",
    sphere: "sphere",
  });
}

function configureClassificationEditorFields(form) {
  configureClassificationFields(form, {
    transactionType: "transaktionstyp",
    topCategory: "oberkategorie",
    subCategory: "unterkategorie",
    sphere: "sphaere",
  });
}

function configureClassificationFields(form, names) {
  const transactionType = form.elements[names.transactionType];
  const topCategory = form.elements[names.topCategory];
  const subCategory = form.elements[names.subCategory];
  const sphere = form.elements[names.sphere];
  if (!transactionType || !topCategory || !subCategory || !sphere) {
    return;
  }

  form.querySelectorAll("datalist[data-classification-options]").forEach(
    (datalist) => datalist.remove(),
  );
  for (const input of [transactionType, topCategory, subCategory]) {
    input.removeAttribute("list");
  }

  const createDatalist = (input, name, values) => {
    const datalist = document.createElement("datalist");
    datalist.dataset.classificationOptions = name;
    datalist.id = `classification-${name}-${ruleDatalistCounter += 1}`;
    for (const value of values) {
      const option = document.createElement("option");
      option.value = value;
      datalist.append(option);
    }
    form.append(datalist);
    input.setAttribute("list", datalist.id);
    return datalist;
  };

  createDatalist(
    transactionType,
    "transaction-types",
    state.classificationOptions.transaction_types || [],
  );
  createDatalist(
    topCategory,
    "top-categories",
    state.classificationOptions.top_categories || [],
  );
  const subcategoryDatalist = createDatalist(
    subCategory,
    "sub-categories",
    [],
  );

  const subcategories = new Map(
    (state.classificationOptions.sub_categories || []).map((entry) => [
      entry.top_category.toLocaleLowerCase("de-DE"),
      entry.values,
    ]),
  );
  const sphereDefaults = new Map(
    (state.classificationOptions.sphere_defaults || []).map((entry) => [
      [
        entry.top_category.toLocaleLowerCase("de-DE"),
        entry.sub_category.toLocaleLowerCase("de-DE"),
      ].join("\u0000"),
      entry.sphere,
    ]),
  );

  const currentSphere = sphere.value;
  sphere.replaceChildren();
  if (!sphere.required) {
    const blank = document.createElement("option");
    blank.value = "";
    blank.textContent = "Nicht angegeben";
    sphere.append(blank);
  }
  for (const value of state.classificationOptions.spheres || []) {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = value;
    sphere.append(option);
  }
  if ([...sphere.options].some((option) => option.value === currentSphere)) {
    sphere.value = currentSphere;
  } else if (!sphere.required) {
    sphere.value = "";
  }

  const refreshSubcategories = () => {
    const topValue = topCategory.value.trim();
    subCategory.disabled = !topValue;
    subcategoryDatalist.replaceChildren();
    const values = subcategories.get(
      topValue.toLocaleLowerCase("de-DE"),
    ) || [];
    for (const value of values) {
      const option = document.createElement("option");
      option.value = value;
      subcategoryDatalist.append(option);
    }
  };

  const applySphereDefault = () => {
    const topValue = topCategory.value.trim();
    const subValue = subCategory.value.trim();
    if (!topValue || !subValue) {
      return;
    }
    const preferred = sphereDefaults.get(
      [
        topValue.toLocaleLowerCase("de-DE"),
        subValue.toLocaleLowerCase("de-DE"),
      ].join("\u0000"),
    );
    if (preferred) {
      sphere.value = preferred;
    }
  };

  topCategory.oninput = () => {
    refreshSubcategories();
    applySphereDefault();
  };
  topCategory.onchange = topCategory.oninput;
  subCategory.oninput = applySphereDefault;
  subCategory.onchange = applySphereDefault;
  refreshSubcategories();
}

function addRuleCondition(
  condition = {},
  container = elements.ruleConditions,
  addButton = elements.ruleAddCondition,
  matchFields = state.ruleMatchFields,
) {
  if (container.children.length >= maxRuleConditions) {
    showError(`Pro Regel sind höchstens ${maxRuleConditions} Bedingungen möglich.`);
    return;
  }
  const row = document.createElement("div");
  row.className = "rule-condition-row";

  const number = document.createElement("strong");
  number.className = "rule-condition-number";

  const connector = document.createElement("select");
  connector.dataset.conditionField = "connector";
  fillSelect(connector, state.ruleLogicConnectors);
  connector.value = condition.connector || "and";
  const connectorField = ruleConditionField("Verknüpfung", connector);
  connectorField.classList.add("rule-condition-connector");

  const matchField = document.createElement("select");
  matchField.dataset.conditionField = "match_field";
  fillSelect(matchField, matchFields);
  if (condition.match_field) {
    matchField.value = condition.match_field;
  }

  const matchOperator = document.createElement("select");
  matchOperator.dataset.conditionField = "match_operator";
  fillSelect(matchOperator, state.ruleMatchOperators);
  if (condition.match_operator) {
    matchOperator.value = condition.match_operator;
  }

  const matchValue = document.createElement("input");
  matchValue.dataset.conditionField = "match_value";
  matchValue.type = "text";
  matchValue.maxLength = 2000;
  matchValue.required = true;
  matchValue.value = condition.match_value || "";
  const suggestionList = document.createElement("datalist");
  suggestionList.dataset.ruleConditionSuggestions = "true";
  suggestionList.id =
    `rule-condition-values-${ruleDatalistCounter += 1}`;

  const remove = document.createElement("button");
  remove.className = "rule-condition-remove";
  remove.type = "button";
  remove.textContent = "Entfernen";
  remove.addEventListener("click", () => {
    row.remove();
    renumberRuleConditions(container, addButton);
    refreshRuleConditionSuggestions(container);
  });

  const refreshSuggestions = () => {
    refreshRuleConditionSuggestions(container);
  };
  connector.addEventListener("change", refreshSuggestions);
  matchField.addEventListener("change", refreshSuggestions);
  matchOperator.addEventListener("change", refreshSuggestions);
  matchValue.addEventListener("input", refreshSuggestions);
  matchValue.addEventListener("change", refreshSuggestions);

  row.append(
    number,
    connectorField,
    ruleConditionField("Vergleichsfeld", matchField),
    ruleConditionField("Operator", matchOperator),
    ruleConditionField("Vergleichswert", matchValue),
    remove,
    suggestionList,
  );
  container.append(row);
  renumberRuleConditions(container, addButton);
  refreshRuleConditionSuggestions(container);
}

function refreshRuleConditionSuggestions(container) {
  const rows = [...container.querySelectorAll(".rule-condition-row")];
  const topCategories = new Set(
    rows
      .filter((row) => {
        const field = row.querySelector(
          '[data-condition-field="match_field"]',
        ).value;
        const connector = row.querySelector(
          '[data-condition-field="connector"]',
        ).value;
        return (
          field === "top_category" &&
          !["and_not", "or_not"].includes(connector)
        );
      })
      .map((row) =>
        row.querySelector(
          '[data-condition-field="match_value"]',
        ).value.trim()
      )
      .filter(Boolean),
  );

  for (const row of rows) {
    const matchField = row.querySelector(
      '[data-condition-field="match_field"]',
    ).value;
    const matchValue = row.querySelector(
      '[data-condition-field="match_value"]',
    );
    const suggestionList = row.querySelector(
      "[data-rule-condition-suggestions]",
    );
    const suggestions = ruleConditionSuggestions(
      matchField,
      topCategories,
    );
    suggestionList.replaceChildren();
    for (const value of suggestions) {
      const option = document.createElement("option");
      option.value = value;
      suggestionList.append(option);
    }
    if (suggestions.length) {
      matchValue.setAttribute("list", suggestionList.id);
    } else {
      matchValue.removeAttribute("list");
    }
  }
}

function ruleConditionSuggestions(matchField, topCategories) {
  if (matchField === "transaction_type") {
    return state.classificationOptions.transaction_types || [];
  }
  if (matchField === "top_category") {
    return state.classificationOptions.top_categories || [];
  }
  if (matchField === "sphere") {
    return state.classificationOptions.spheres || [];
  }
  if (matchField !== "sub_category") {
    return [];
  }

  const entries = state.classificationOptions.sub_categories || [];
  const normalizedTopCategories = new Set(
    [...topCategories].map((value) =>
      value.toLocaleLowerCase("de-DE")
    ),
  );
  const relevantEntries = normalizedTopCategories.size
    ? entries.filter((entry) =>
      normalizedTopCategories.has(
        entry.top_category.toLocaleLowerCase("de-DE"),
      )
    )
    : entries;
  return [...new Set(
    relevantEntries.flatMap((entry) => entry.values || []),
  )].sort((left, right) =>
    left.localeCompare(right, "de-DE", {sensitivity: "base"})
  );
}

function ruleConditionField(labelText, control) {
  const label = document.createElement("label");
  const text = document.createElement("span");
  text.textContent = labelText;
  label.append(text, control);
  return label;
}

function renumberRuleConditions(
  container = elements.ruleConditions,
  addButton = elements.ruleAddCondition,
) {
  const rows = [...container.children];
  rows.forEach((row, index) => {
    row.querySelector(".rule-condition-number").textContent =
      `Bedingung ${index + 1}`;
    const connectorField = row.querySelector(".rule-condition-connector");
    const connector = row.querySelector('[data-condition-field="connector"]');
    connectorField.hidden = index === 0;
    connector.disabled = index === 0;
    if (index === 0) {
      connector.value = "";
    } else if (!connector.value) {
      connector.value = "and";
    }
    const remove = row.querySelector(".rule-condition-remove");
    remove.disabled = rows.length === 1;
    remove.setAttribute(
      "aria-label",
      `Bedingung ${index + 1} entfernen`,
    );
  });
  addButton.disabled = rows.length >= maxRuleConditions;
}

function readRuleConditions(container = elements.ruleConditions) {
  const conditions = [...container.children].map(
    (row, index) => ({
      connector: index === 0
        ? ""
        : row.querySelector(
          '[data-condition-field="connector"]',
        ).value,
      match_field: row.querySelector(
        '[data-condition-field="match_field"]',
      ).value,
      match_operator: row.querySelector(
        '[data-condition-field="match_operator"]',
      ).value,
      match_value: row.querySelector(
        '[data-condition-field="match_value"]',
      ).value.trim(),
    }),
  );
  validateRuleConditions(conditions);
  return conditions;
}

function validateRuleConditions(conditions) {
  if (!conditions.length) {
    throw new Error("Die Regel benötigt mindestens eine Bedingung.");
  }
  const connectors = new Set(["and", "or", "and_not", "or_not"]);
  const groups = [[]];
  conditions.forEach((condition, index) => {
    if (
      !condition.match_field ||
      !condition.match_operator ||
      !condition.match_value
    ) {
      throw new Error(
        `Bedingung ${index + 1} ist nicht vollständig ausgefüllt.`,
      );
    }
    if (index > 0 && !connectors.has(condition.connector)) {
      throw new Error(
        `Bedingung ${index + 1} hat keine gültige Verknüpfung.`,
      );
    }
    const negated = ["and_not", "or_not"].includes(condition.connector);
    if (
      index > 0 &&
      ["or", "or_not"].includes(condition.connector)
    ) {
      groups.push([]);
    }
    const key = [
      condition.match_field,
      condition.match_operator,
      condition.match_value.replace(/\s+/g, " ").toLocaleLowerCase("de-DE"),
    ].join("\u0000");
    const group = groups.at(-1);
    if (
      group.some(
        (entry) => entry.key === key && entry.negated !== negated,
      )
    ) {
      throw new Error(
        "Eine UND-Gruppe darf dieselbe Bedingung nicht zugleich " +
        "verlangen und ausschließen.",
      );
    }
    group.push({key, negated});
  });
  const singletonGroups = new Map();
  groups.filter((group) => group.length === 1).forEach((group) => {
    const {key, negated} = group[0];
    if (
      singletonGroups.has(key) &&
      singletonGroups.get(key) !== negated
    ) {
      throw new Error(
        "Diese ODER-Verknüpfung wäre immer wahr, weil sie eine " +
        "Bedingung mit ihrem Gegenteil kombiniert.",
      );
    }
    singletonGroups.set(key, negated);
  });
}

async function createRule(event) {
  event.preventDefault();
  const submit = elements.ruleForm.querySelector('[type="submit"]');
  submit.disabled = true;
  const editing = Boolean(state.editingRuleId);
  elements.ruleFormStatus.textContent = editing
    ? "Regel wird gespeichert"
    : "Regel wird erstellt";
  const formData = new FormData(elements.ruleForm);
  const payload = Object.fromEntries(formData.entries());
  payload.enabled = elements.ruleForm.elements.enabled.checked;
  payload.apply_now = elements.ruleForm.elements.apply_now.checked;
  try {
    payload.conditions = readRuleConditions();
    const endpoint = editing
      ? `/api/rules/${encodeURIComponent(state.editingRuleId)}`
      : "/api/rules";
    const response = await fetch(endpoint, {
      method: editing ? "PATCH" : "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload),
    });
    const result = await readResponse(response);
    const resultMessage = result.applied
      ? `${result.changed_transactions} Transaktionen klassifiziert`
      : editing ? "Regel aktualisiert" : "Regel gespeichert";
    resetRuleForm();
    state.rulesLoaded = false;
    await loadRules();
    elements.ruleFormStatus.textContent = resultMessage;
    if (result.changed_transactions) {
      loadTransactions();
      state.vorgaengeLoaded = false;
    }
  } catch (error) {
    elements.ruleFormStatus.textContent = editing
      ? "Speichern fehlgeschlagen"
      : "Erstellen fehlgeschlagen";
    showError(error.message);
  } finally {
    submit.disabled = false;
  }
}

async function deleteRule(rule) {
  if (!window.confirm(`Regel "${rule.name}" wirklich entfernen?`)) {
    return;
  }
  elements.ruleFormStatus.textContent = "Regel wird entfernt";
  try {
    const response = await fetch(
      `/api/rules/${encodeURIComponent(rule.rule_id)}`,
      {method: "DELETE"},
    );
    await readResponse(response);
    if (state.editingRuleId === rule.rule_id) {
      resetRuleForm();
    }
    state.rulesLoaded = false;
    await loadRules();
    elements.ruleFormStatus.textContent = "Regel entfernt";
  } catch (error) {
    elements.ruleFormStatus.textContent = "Entfernen fehlgeschlagen";
    showError(error.message);
  }
}

function editRule(rule) {
  state.editingRuleId = rule.rule_id;
  elements.ruleFormTitle.textContent = `Regel bearbeiten: ${rule.name}`;
  elements.ruleSubmit.textContent = "Änderungen speichern";
  elements.ruleCancelEdit.hidden = false;
  for (const field of [
    "name",
    "transaction_type",
    "top_category",
    "sub_category",
    "sphere",
    "professional_description",
  ]) {
    elements.ruleForm.elements[field].value = rule[field] || "";
  }
  elements.ruleForm.elements.enabled.checked = rule.enabled;
  elements.ruleForm.elements.apply_now.checked = false;
  const conditions = rule.conditions?.length
    ? rule.conditions
    : [{
      connector: "",
      match_field: rule.match_field,
      match_operator: rule.match_operator,
      match_value: rule.match_value,
    }];
  elements.ruleConditions.replaceChildren();
  conditions.forEach((condition) => addRuleCondition(condition));
  configureRuleClassificationFields(elements.ruleForm);
  elements.ruleFormStatus.textContent =
    "Felder bearbeiten und anschließend speichern";
  elements.ruleForm.scrollIntoView({behavior: "smooth", block: "start"});
}

function resetRuleForm() {
  state.editingRuleId = null;
  elements.ruleForm.reset();
  elements.ruleConditions.replaceChildren();
  if (Object.keys(state.ruleMatchFields).length) {
    addRuleCondition();
  }
  elements.ruleForm.elements.enabled.checked = true;
  elements.ruleForm.elements.apply_now.checked = true;
  configureRuleClassificationFields(elements.ruleForm);
  elements.ruleFormTitle.textContent = "Neue Regel";
  elements.ruleSubmit.textContent = "Regel erstellen";
  elements.ruleCancelEdit.hidden = true;
  elements.ruleFormStatus.textContent = "";
}

async function createCompletionRule(event) {
  event.preventDefault();
  const submit = elements.completionRuleSubmit;
  submit.disabled = true;
  const editing = Boolean(state.editingCompletionRuleId);
  elements.completionRuleFormStatus.textContent = editing
    ? "Abschlussregel wird gespeichert"
    : "Abschlussregel wird erstellt";
  const payload = Object.fromEntries(
    new FormData(elements.completionRuleForm).entries(),
  );
  payload.enabled = elements.completionRuleForm.elements.enabled.checked;
  payload.apply_now =
    elements.completionRuleForm.elements.apply_now.checked;
  try {
    payload.conditions = readRuleConditions(
      elements.completionRuleConditions,
    );
    const endpoint = editing
      ? `/api/completion-rules/${encodeURIComponent(
        state.editingCompletionRuleId,
      )}`
      : "/api/completion-rules";
    const response = await fetch(endpoint, {
      method: editing ? "PATCH" : "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload),
    });
    const result = await readResponse(response);
    const message = result.applied
      ? `${result.changed_vorgaenge} Vorgänge aktualisiert`
      : editing
        ? "Abschlussregel aktualisiert"
        : "Abschlussregel gespeichert";
    resetCompletionRuleForm();
    state.rulesLoaded = false;
    await loadRules();
    elements.completionRuleFormStatus.textContent = message;
    loadTransactions();
    state.vorgaengeLoaded = false;
    if (!elements.vorgaengePanel.hidden) {
      loadVorgaenge();
    }
  } catch (error) {
    elements.completionRuleFormStatus.textContent = editing
      ? "Speichern fehlgeschlagen"
      : "Erstellen fehlgeschlagen";
    showError(error.message);
  } finally {
    submit.disabled = false;
  }
}

async function deleteCompletionRule(rule) {
  if (!window.confirm(
    `Abschlussregel "${rule.name}" wirklich entfernen?`,
  )) {
    return;
  }
  elements.completionRuleFormStatus.textContent =
    "Abschlussregel wird entfernt";
  try {
    const response = await fetch(
      `/api/completion-rules/${encodeURIComponent(rule.rule_id)}`,
      {method: "DELETE"},
    );
    const result = await readResponse(response);
    if (state.editingCompletionRuleId === rule.rule_id) {
      resetCompletionRuleForm();
    }
    state.rulesLoaded = false;
    await loadRules();
    elements.completionRuleFormStatus.textContent =
      `Abschlussregel entfernt, ${result.changed_vorgaenge} Vorgänge aktualisiert`;
    state.vorgaengeLoaded = false;
    if (!elements.vorgaengePanel.hidden) {
      loadVorgaenge();
    }
  } catch (error) {
    elements.completionRuleFormStatus.textContent =
      "Entfernen fehlgeschlagen";
    showError(error.message);
  }
}

function editCompletionRule(rule) {
  state.editingCompletionRuleId = rule.rule_id;
  elements.completionRuleFormTitle.textContent =
    `Abschlussregel bearbeiten: ${rule.name}`;
  elements.completionRuleSubmit.textContent = "Änderungen speichern";
  elements.completionRuleCancelEdit.hidden = false;
  elements.completionRuleForm.elements.name.value = rule.name;
  elements.completionRuleForm.elements.enabled.checked = rule.enabled;
  elements.completionRuleForm.elements.apply_now.checked = true;
  const conditions = rule.conditions?.length
    ? rule.conditions
    : [{
      connector: "",
      match_field: rule.match_field,
      match_operator: rule.match_operator,
      match_value: rule.match_value,
    }];
  elements.completionRuleConditions.replaceChildren();
  conditions.forEach((condition) => {
    addRuleCondition(
      condition,
      elements.completionRuleConditions,
      elements.completionRuleAddCondition,
      state.completionRuleMatchFields,
    );
  });
  elements.completionRuleFormStatus.textContent =
    "Felder bearbeiten und anschließend speichern";
  elements.completionRuleForm.scrollIntoView({
    behavior: "smooth",
    block: "start",
  });
}

function resetCompletionRuleForm() {
  state.editingCompletionRuleId = null;
  elements.completionRuleForm.reset();
  elements.completionRuleConditions.replaceChildren();
  if (Object.keys(state.completionRuleMatchFields).length) {
    addRuleCondition(
      {},
      elements.completionRuleConditions,
      elements.completionRuleAddCondition,
      state.completionRuleMatchFields,
    );
  }
  elements.completionRuleForm.elements.enabled.checked = true;
  elements.completionRuleForm.elements.apply_now.checked = true;
  elements.completionRuleFormTitle.textContent = "Neue Abschlussregel";
  elements.completionRuleSubmit.textContent = "Abschlussregel erstellen";
  elements.completionRuleCancelEdit.hidden = true;
  elements.completionRuleFormStatus.textContent = "";
}

async function requestRefresh() {
  setRefreshButtonsDisabled(true);
  setRefreshStatus("Aktualisierung wird gestartet");
  try {
    const response = await fetch("/api/refresh", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: "{}",
    });
    const payload = await readResponse(response);
    renderRefreshStatus(payload);
    scheduleRefreshPoll();
  } catch (error) {
    setRefreshButtonsDisabled(false);
    setRefreshStatus(error.message, "error");
    showError(error.message);
  }
}

function scheduleRefreshPoll(delay = 1500) {
  clearTimeout(refreshTimer);
  refreshTimer = setTimeout(loadRefreshStatus, delay);
}

async function loadRefreshStatus() {
  try {
    const response = await fetch("/api/refresh");
    const payload = await readResponse(response);
    renderRefreshStatus(payload);
    if (payload.status === "running") {
      scheduleRefreshPoll();
    }
  } catch (error) {
    setRefreshButtonsDisabled(false);
    setRefreshStatus(error.message, "error");
  }
}

function renderRefreshStatus(payload) {
  if (!payload.available) {
    setRefreshButtonsDisabled(true);
    setRefreshStatus("Keine Bankkonfiguration für Aktualisierungen gefunden.");
    return;
  }
  if (payload.status === "running") {
    setRefreshButtonsDisabled(true);
    setRefreshStatus(payload.message);
    return;
  }
  setRefreshButtonsDisabled(false);
  if (payload.status === "completed") {
    const newCount = payload.result?.new_transactions ?? 0;
    setRefreshStatus(
      `${payload.message} ${newCount} neue Transaktionen.`,
      "success",
    );
    loadOverview();
    loadTransactions();
    state.vorgaengeLoaded = false;
    if (!elements.vorgaengePanel.hidden) {
      loadVorgaenge();
    }
    if (!elements.balanceHistoryPanel.hidden) {
      loadBalanceHistory();
    } else {
      state.balanceHistory = null;
    }
    return;
  }
  if (payload.status === "failed") {
    setRefreshStatus(payload.message, "error");
    return;
  }
  setRefreshStatus("");
}

function setRefreshStatus(message, type = "") {
  for (const target of [
    elements.refreshStatus,
    elements.dashboardRefreshStatus,
  ]) {
    target.textContent = message;
    target.className = type ? `is-${type}` : "";
  }
}

function setRefreshButtonsDisabled(disabled) {
  elements.refreshTransactions.disabled = disabled;
  elements.dashboardRefresh.disabled = disabled;
}

async function loadPlayerPremiumStatus() {
  try {
    const response = await fetch("/api/player-premiums");
    const payload = await readResponse(response);
    renderPlayerPremiumConfiguration(payload);
    renderPlayerPremiumStatus(payload);
    state.playerPremiumLoaded = true;
    if (payload.status === "running") {
      schedulePlayerPremiumPoll();
    }
  } catch (error) {
    setPlayerPremiumStatus(error.message, "error");
    showError(error.message);
  }
}

function renderPlayerPremiumConfiguration(payload) {
  if (!elements.playerPremiumSeason.options.length) {
    for (const season of payload.seasons || []) {
      const option = document.createElement("option");
      option.value = season;
      option.textContent = season;
      elements.playerPremiumSeason.append(option);
    }
  }
  if (!elements.playerPremiumTeams.children.length) {
    for (const team of payload.teams || []) {
      const option = document.createElement("div");
      option.className = "premium-team-option";
      const label = document.createElement("label");
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.name = "team_ids";
      checkbox.value = team.team_id;
      checkbox.checked = true;
      const text = document.createElement("span");
      const title = document.createElement("strong");
      title.textContent = team.label;
      const dfbnetName = document.createElement("small");
      dfbnetName.textContent = team.dfbnet_name;
      text.append(title, dfbnetName);
      label.append(checkbox, text);
      const rateLabel = document.createElement("label");
      rateLabel.className = "premium-point-value";
      const rateText = document.createElement("span");
      rateText.textContent = "Summe pro Punkt";
      const rateControl = document.createElement("span");
      rateControl.className = "premium-point-value-control";
      const rateInput = document.createElement("input");
      rateInput.type = "number";
      rateInput.name = "point_value";
      rateInput.dataset.teamId = team.team_id;
      rateInput.min = "0";
      rateInput.max = "10000";
      rateInput.step = "0.01";
      rateInput.required = true;
      rateInput.value = Number(team.default_point_value).toFixed(2);
      const currency = document.createElement("span");
      currency.textContent = "€";
      rateControl.append(rateInput, currency);
      rateLabel.append(rateText, rateControl);
      checkbox.addEventListener("change", () => {
        rateInput.disabled = !checkbox.checked;
        option.classList.toggle("is-disabled", !checkbox.checked);
      });
      option.append(label, rateLabel);
      elements.playerPremiumTeams.append(option);
    }
  }
}

async function requestPlayerPremiums(event) {
  event.preventDefault();
  const teamIds = [
    ...elements.playerPremiumTeams.querySelectorAll(
      'input[name="team_ids"]:checked',
    ),
  ].map((checkbox) => checkbox.value);
  if (!teamIds.length) {
    showError("Mindestens eine Mannschaft muss ausgewählt werden.");
    return;
  }
  const pointValues = {};
  for (const teamId of teamIds) {
    const input = elements.playerPremiumTeams.querySelector(
      `input[name="point_value"][data-team-id="${teamId}"]`,
    );
    const value = Number(input?.value);
    if (!input || !Number.isFinite(value) || value < 0) {
      showError("Bitte eine gültige Summe pro Punkt eingeben.");
      input?.focus();
      return;
    }
    pointValues[teamId] = input.value;
  }
  elements.playerPremiumSubmit.disabled = true;
  setPlayerPremiumStatus("Auswertung wird gestartet");
  try {
    const response = await fetch("/api/player-premiums", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        season: elements.playerPremiumSeason.value,
        team_ids: teamIds,
        point_values: pointValues,
      }),
    });
    const payload = await readResponse(response);
    renderPlayerPremiumStatus(payload);
    schedulePlayerPremiumPoll();
  } catch (error) {
    elements.playerPremiumSubmit.disabled = false;
    setPlayerPremiumStatus(error.message, "error");
    showError(error.message);
  }
}

function schedulePlayerPremiumPoll(delay = 1500) {
  clearTimeout(playerPremiumTimer);
  playerPremiumTimer = setTimeout(loadPlayerPremiumStatus, delay);
}

function renderPlayerPremiumStatus(payload) {
  if (!payload.available) {
    elements.playerPremiumSubmit.disabled = true;
    elements.playerPremiumLoading.hidden = true;
    setPlayerPremiumStatus(
      "DFBnet-Auswertung ist für diesen Dashboard-Start nicht konfiguriert.",
    );
    return;
  }
  if (payload.status === "running") {
    elements.playerPremiumSubmit.disabled = true;
    elements.playerPremiumLoading.hidden = false;
    setPlayerPremiumStatus(payload.message);
    return;
  }
  elements.playerPremiumSubmit.disabled = false;
  elements.playerPremiumLoading.hidden = true;
  if (payload.status === "completed" && payload.result) {
    setPlayerPremiumStatus(payload.message, "success");
    renderPlayerPremiumResult(payload.result);
    return;
  }
  if (payload.status === "failed") {
    setPlayerPremiumStatus(payload.message, "error");
    return;
  }
  setPlayerPremiumStatus("");
}

function setPlayerPremiumStatus(message, type = "") {
  elements.playerPremiumStatus.textContent = message;
  elements.playerPremiumStatus.className = type ? `is-${type}` : "";
}

function renderPlayerPremiumResult(result) {
  elements.playerPremiumTables.replaceChildren();
  elements.playerPremiumResultMeta.textContent =
    `${result.season} · erstellt ${formatDateTime(result.generated_at)}`;
  for (const team of result.teams || []) {
    const section = document.createElement("section");
    section.className = "premium-team-result";
    const heading = document.createElement("div");
    heading.className = "premium-result-heading";
    const title = document.createElement("h5");
    title.textContent = team.label;
    const detail = document.createElement("span");
    detail.textContent =
      `${integerFormatter.format(team.matches.length)} Spiele · ` +
      `${integerFormatter.format(team.team_points_total || 0)} Mannschaftspunkte · ` +
      `${integerFormatter.format(team.players.length)} Spieler · ` +
      `${currencyFormatter.format(Number(team.point_value))}/Punkt · ` +
      `${currencyFormatter.format(Number(team.premium_total))} gesamt`;
    heading.append(title, detail);
    section.append(heading);
    const completenessWarnings = team.completeness?.warnings || [];
    if (completenessWarnings.length) {
      const warning = document.createElement("div");
      warning.className = "premium-completeness-warning";
      warning.textContent = completenessWarnings.join(" ");
      section.append(warning);
    }

    if (!team.matches.length) {
      section.append(
        premiumEmptyMessage("Für diese Mannschaft wurden keine Spiele gefunden."),
      );
      elements.playerPremiumTables.append(section);
      continue;
    }
    if (!team.players.length) {
      section.append(
        premiumEmptyMessage(
          "Für diese Mannschaft konnten keine Aufstellungen ermittelt werden.",
        ),
      );
      elements.playerPremiumTables.append(section);
      continue;
    }

    const frame = document.createElement("div");
    frame.className = "premium-table-frame";
    const table = document.createElement("table");
    table.className = "premium-table";
    const head = document.createElement("thead");
    const headRow = document.createElement("tr");
    const playerHeading = document.createElement("th");
    playerHeading.textContent = "Spieler";
    headRow.append(playerHeading);
    for (const match of team.matches) {
      const cell = document.createElement("th");
      cell.title = [
        formatDate(match.date),
        match.competition,
        match.pairing || match.opponent,
        match.result,
        `${match.team_points ?? match.points ?? 0} Mannschaftspunkte`,
      ].filter(Boolean).join(" · ");
      const label = document.createElement("strong");
      label.textContent = match.label;
      const resultText = document.createElement("small");
      const teamPoints = Number(match.team_points ?? match.points ?? 0);
      resultText.textContent = [
        formatDate(match.date),
        match.pairing || match.opponent,
        match.result,
        `${integerFormatter.format(teamPoints)} Pkt.`,
      ].filter(Boolean).join(" · ");
      cell.append(label, resultText);
      headRow.append(cell);
    }
    const totalHeading = document.createElement("th");
    totalHeading.textContent = "Gesamt";
    headRow.append(totalHeading);
    head.append(headRow);

    const body = document.createElement("tbody");
    for (const player of team.players) {
      const row = document.createElement("tr");
      const name = document.createElement("th");
      name.scope = "row";
      name.textContent = player.name;
      row.append(name);
      for (const match of team.matches) {
        const cell = document.createElement("td");
        const value = player.values[match.match_id];
        if (value === null || value === undefined) {
          cell.className = "is-empty";
          cell.textContent = "";
        } else {
          const pointClass = {
            0: "is-zero",
            1: "is-one",
            3: "is-three",
          }[value] || "";
          cell.className = `premium-points ${pointClass}`.trim();
          const premium = player.premium_values?.[match.match_id] ?? 0;
          const amount = document.createElement("strong");
          amount.textContent = currencyFormatter.format(Number(premium));
          const points = document.createElement("small");
          points.textContent = `${value} ${value === 1 ? "Punkt" : "Punkte"}`;
          cell.append(amount, points);
        }
        row.append(cell);
      }
      const total = document.createElement("td");
      total.className = "premium-total";
      const totalAmount = document.createElement("strong");
      totalAmount.textContent = currencyFormatter.format(
        Number(player.premium_total),
      );
      const totalPoints = document.createElement("small");
      totalPoints.textContent =
        `${integerFormatter.format(player.total)} Punkte`;
      total.append(totalAmount, totalPoints);
      row.append(total);
      body.append(row);
    }
    table.append(head, body);
    frame.append(table);
    section.append(frame);
    elements.playerPremiumTables.append(section);
  }
  elements.playerPremiumResults.hidden = false;
}

function premiumEmptyMessage(message) {
  const paragraph = document.createElement("p");
  paragraph.className = "premium-empty";
  paragraph.textContent = message;
  return paragraph;
}

async function loadPlayerPaymentStatus() {
  try {
    const response = await fetch("/api/player-premium-payments");
    const payload = await readResponse(response);
    renderPlayerPaymentStatus(payload);
    state.playerPaymentLoaded = true;
    if (payload.status === "running") {
      schedulePlayerPaymentPoll();
    }
  } catch (error) {
    setPlayerPaymentStatus(error.message, "error");
    showError(error.message);
  }
}

async function requestPlayerPayments() {
  elements.playerPaymentSubmit.disabled = true;
  elements.playerOffsetManualList.replaceChildren();
  state.manualOffsetCounter = 0;
  state.playerPaymentResult = null;
  setPaymentOffsetControls(false);
  setPlayerPaymentStatus("Zahlungsdaten-Prüfung wird gestartet");
  try {
    const response = await fetch("/api/player-premium-payments", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        deckel_path: elements.playerOffsetDeckelPath.value,
      }),
    });
    const payload = await readResponse(response);
    renderPlayerPaymentStatus(payload);
    schedulePlayerPaymentPoll();
  } catch (error) {
    elements.playerPaymentSubmit.disabled = false;
    setPlayerPaymentStatus(error.message, "error");
    showError(error.message);
  }
}

function schedulePlayerPaymentPoll(delay = 1500) {
  clearTimeout(playerPaymentTimer);
  playerPaymentTimer = setTimeout(loadPlayerPaymentStatus, delay);
}

function renderPlayerPaymentStatus(payload) {
  state.playerPaymentManualAvailable = Boolean(payload.manual_available);
  if (!payload.available && !payload.result) {
    elements.playerPaymentSubmit.disabled = true;
    elements.playerPaymentLoading.hidden = true;
    setPaymentOffsetControls(false);
    setPlayerPaymentStatus(
      "Die Zahlungsdaten-Prüfung ist für diesen Dashboard-Start nicht konfiguriert.",
    );
    return;
  }
  if (payload.status === "running") {
    elements.playerPaymentSubmit.disabled = true;
    elements.playerPaymentLoading.hidden = false;
    setPaymentOffsetControls(false);
    setPlayerPaymentStatus(payload.message);
    return;
  }
  elements.playerPaymentSubmit.disabled = !payload.available;
  elements.playerPaymentLoading.hidden = true;
  if (payload.status === "completed" && payload.result) {
    setPlayerPaymentStatus(payload.message, "success");
    renderPlayerPaymentResult(payload.result);
    return;
  }
  if (payload.status === "failed") {
    setPaymentOffsetControls(false);
    setPlayerPaymentStatus(payload.message, "error");
    return;
  }
  setPaymentOffsetControls(false);
  setPlayerPaymentStatus("");
}

function setPlayerPaymentStatus(message, type = "") {
  elements.playerPaymentStatus.textContent = message;
  elements.playerPaymentStatus.className = type ? `is-${type}` : "";
}

function setPlayerOffsetStatus(message, type = "") {
  elements.playerOffsetStatus.textContent = message;
  elements.playerOffsetStatus.className = type ? `is-${type}` : "";
}

function markPlayerOffsetsPending() {
  if (elements.playerOffsetPanel.hidden) {
    return;
  }
  setPlayerOffsetStatus(
    "Änderungen noch nicht bestätigt.",
    "pending",
  );
}

function setPaymentOffsetControls(available) {
  elements.playerOffsetPanel.hidden = !available;
  elements.playerOffsetApply.disabled = !available;
  elements.playerOffsetAddManual.disabled = !available;
  elements.playerPaymentExport.disabled = !available;
}

function renderPlayerPaymentResult(result) {
  state.playerPaymentResult = result;
  setPaymentOffsetControls(true);
  if (!elements.playerOffsetDeckelPath.value && result.default_deckel_path) {
    elements.playerOffsetDeckelPath.value = result.default_deckel_path;
  }
  const counts = result.counts || {};
  const totals = result.totals || {};
  elements.playerPaymentSummary.replaceChildren(
    paymentSummaryItem(
      "Eindeutig",
      counts.eindeutig_gefunden || 0,
      "is-valid",
    ),
    paymentSummaryItem(
      "Manuell prüfen",
      counts.manuell_pruefen || 0,
      "is-review",
    ),
    paymentSummaryItem(
      "Nicht gefunden",
      counts.nicht_gefunden || 0,
      "is-missing",
    ),
    paymentSummaryItem(
      "Prämien",
      currencyFormatter.format(Number(totals.premium_total || 0)),
      "is-neutral",
    ),
    paymentSummaryItem(
      "Verrechnet",
      currencyFormatter.format(Number(totals.offset_total || 0)),
      "is-review",
    ),
    paymentSummaryItem(
      "Überweisung",
      currencyFormatter.format(Number(totals.transfer_total || 0)),
      "is-valid",
    ),
    paymentSummaryItem(
      "Lastschrift",
      currencyFormatter.format(Number(totals.debit_total || 0)),
      "is-missing",
    ),
    paymentSummaryItem(
      "Deckel extern",
      currencyFormatter.format(Number(totals.deckel_external_debit_total || 0)),
      "is-review",
    ),
  );
  renderPlayerOffsetReview(result);
  elements.playerPaymentTeams.replaceChildren();
  const groups = result.team_groups?.length
    ? result.team_groups
    : [{
      team_id: "alle",
      label: "Spieler",
      players: result.players || [],
    }];
  for (const group of groups) {
    elements.playerPaymentTeams.append(paymentTeamSection(group));
  }
  elements.playerPaymentResults.hidden = false;
}

function renderPlayerOffsetReview(result) {
  elements.playerOffsetReview.replaceChildren();
  const configuration = result.offset_configuration || {};
  const positions = configuration.deckel_positions || [];
  if (configuration.deckel_path && elements.playerOffsetDeckelPath.value !== configuration.deckel_path) {
    elements.playerOffsetDeckelPath.value = configuration.deckel_path;
  }
  if (!positions.length) {
    const empty = document.createElement("p");
    empty.className = "payment-offset-empty";
    empty.textContent =
      "Noch keine Deckellistenpositionen geprüft.";
    elements.playerOffsetReview.append(empty);
    return;
  }

  const frame = document.createElement("div");
  frame.className = "payment-offset-frame";
  const table = document.createElement("table");
  table.className = "payment-offset-table";
  const head = document.createElement("thead");
  const heading = document.createElement("tr");
  for (const label of ["Deckelliste", "Betrag", "Zuordnung", "Vorschlag", "Bankdaten"]) {
    const cell = document.createElement("th");
    cell.textContent = label;
    heading.append(cell);
  }
  head.append(heading);
  const body = document.createElement("tbody");
  for (const position of positions) {
    const row = document.createElement("tr");
    const name = document.createElement("th");
    name.scope = "row";
    name.textContent = position.raw_name || "Ohne Namen";
    const amount = document.createElement("td");
    amount.textContent = currencyFormatter.format(Number(position.amount || 0));

    const assignment = document.createElement("td");
    const select = document.createElement("select");
    select.dataset.offsetAssignment = position.position_id || "";
    fillPaymentPlayerOptions(select, position.assigned_premium_name || "");
    assignment.append(select);
    assignment.append(
      paymentStatusBadge(
        formatOffsetAssignment(position.assignment_status),
        offsetAssignmentClass(position.assignment_status),
      ),
    );

    const suggestion = document.createElement("td");
    const suggested = position.best_premium_name || "Kein eindeutiger Vorschlag";
    suggestion.textContent = suggested;
    const score = document.createElement("small");
    score.textContent = position.match_score
      ? `${Math.round(Number(position.match_score) * 100)} %`
      : "";
    suggestion.append(score);
    const bank = document.createElement("td");
    bank.append(deckelExternalBankStatus(position));
    row.append(name, amount, assignment, suggestion, bank);
    body.append(row);
  }
  table.append(head, body);
  frame.append(table);
  elements.playerOffsetReview.append(frame);
}

function deckelExternalBankStatus(position) {
  const container = document.createElement("div");
  const debtor = position.external_debtor || {};
  if (position.assignment_status !== "unassigned") {
    const assigned = document.createElement("span");
    assigned.className = "is-neutral";
    assigned.textContent = "Wird beim Spieler verrechnet";
    container.append(assigned);
    return container;
  }
  if (!debtor.member_name && !debtor.masked_iban) {
    const missing = paymentStatusBadge("Nicht gefunden", "is-missing");
    container.append(missing);
    return container;
  }
  container.append(
    paymentStatusBadge(
      debtor.iban_valid && debtor.bic_valid ? "Lastschrift bereit" : "Prüfen",
      debtor.iban_valid && debtor.bic_valid ? "is-valid" : "is-review",
    ),
  );
  const member = document.createElement("small");
  member.textContent = debtor.member_name || debtor.premium_name || "";
  const iban = document.createElement("small");
  iban.className = "is-monospace";
  iban.textContent = debtor.masked_iban || "Keine IBAN";
  container.append(member, iban);
  return container;
}

function fillPaymentPlayerOptions(select, selectedValue = "") {
  select.replaceChildren();
  const empty = document.createElement("option");
  empty.value = "";
  empty.textContent = "Nicht zugeordnet";
  select.append(empty);
  for (const player of state.playerPaymentResult?.players || []) {
    const option = document.createElement("option");
    option.value = player.premium_name || "";
    option.textContent = player.premium_name || "";
    option.selected = option.value === selectedValue;
    select.append(option);
  }
}

function addManualOffsetRow(offset = {}) {
  const players = state.playerPaymentResult?.players || [];
  if (!players.length) {
    setPlayerOffsetStatus("Noch keine Zahlungsdaten geladen.", "error");
    return;
  }
  const row = document.createElement("div");
  row.className = "payment-manual-offset-row";
  row.dataset.manualOffset = String(++state.manualOffsetCounter);

  const playerLabel = manualOffsetField("Spieler");
  const playerSelect = document.createElement("select");
  fillPaymentPlayerOptions(playerSelect, offset.premium_name || "");
  playerLabel.append(playerSelect);

  const labelField = manualOffsetField("Bezeichnung");
  const labelInput = document.createElement("input");
  labelInput.type = "text";
  labelInput.maxLength = 200;
  labelInput.value = offset.label || "";
  labelInput.placeholder = "Sonstige Gegenposition";
  labelField.append(labelInput);

  const amountField = manualOffsetField("Betrag");
  const amountInput = document.createElement("input");
  amountInput.type = "number";
  amountInput.step = "0.01";
  amountInput.min = "0";
  amountInput.inputMode = "decimal";
  amountInput.value = offset.amount || "";
  amountInput.placeholder = "Wird abgezogen";
  amountField.append(amountInput);

  const transactionType = manualOffsetInput(
    "Transaktionstyp",
    offset.classification?.transaction_type || "",
  );
  const topCategory = manualOffsetInput(
    "Oberkategorie",
    offset.classification?.top_category || "",
  );
  const subCategory = manualOffsetInput(
    "Unterkategorie",
    offset.classification?.sub_category || "",
  );
  const sphere = manualOffsetInput(
    "Sphäre",
    offset.classification?.sphere || "",
  );

  const remove = document.createElement("button");
  remove.type = "button";
  remove.className = "payment-offset-remove";
  remove.textContent = "Entfernen";
  remove.addEventListener("click", () => {
    row.remove();
    markPlayerOffsetsPending();
  });

  row.append(
    playerLabel,
    labelField,
    amountField,
    transactionType.label,
    topCategory.label,
    subCategory.label,
    sphere.label,
    remove,
  );
  row._manualOffsetControls = {
    playerSelect,
    labelInput,
    amountInput,
    transactionType: transactionType.input,
    topCategory: topCategory.input,
    subCategory: subCategory.input,
    sphere: sphere.input,
  };
  elements.playerOffsetManualList.append(row);
}

function manualOffsetField(labelText) {
  const label = document.createElement("label");
  const span = document.createElement("span");
  span.textContent = labelText;
  label.append(span);
  return label;
}

function manualOffsetInput(labelText, value) {
  const label = manualOffsetField(labelText);
  const input = document.createElement("input");
  input.type = "text";
  input.maxLength = 120;
  input.value = value;
  label.append(input);
  return {label, input};
}

function collectPlayerPaymentOffsetPayload() {
  const assignments = {};
  for (const select of elements.playerOffsetReview.querySelectorAll(
    "select[data-offset-assignment]",
  )) {
    assignments[select.dataset.offsetAssignment] = select.value;
  }
  const manualOffsets = [];
  for (const row of elements.playerOffsetManualList.querySelectorAll(
    "[data-manual-offset]",
  )) {
    const controls = row._manualOffsetControls;
    if (!controls || !controls.amountInput.value) {
      continue;
    }
    manualOffsets.push({
      premium_name: controls.playerSelect.value,
      label: controls.labelInput.value,
      amount: controls.amountInput.value,
      classification: {
        transaction_type: controls.transactionType.value,
        top_category: controls.topCategory.value,
        sub_category: controls.subCategory.value,
        sphere: controls.sphere.value,
      },
    });
  }
  return {
    deckel_path: elements.playerOffsetDeckelPath.value,
    use_deckel: true,
    assignments,
    manual_offsets: manualOffsets,
  };
}

async function submitPlayerPaymentOffsets() {
  const response = await fetch("/api/player-premium-payments/offsets", {
    method: "PATCH",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(collectPlayerPaymentOffsetPayload()),
  });
  const payload = await readResponse(response);
  renderPlayerPaymentStatus(payload);
  return payload;
}

async function applyPlayerPaymentOffsets() {
  elements.playerOffsetApply.disabled = true;
  elements.playerPaymentExport.disabled = true;
  setPlayerOffsetStatus("Verrechnungen werden geprüft");
  try {
    await submitPlayerPaymentOffsets();
    setPlayerOffsetStatus("Verrechnungen wurden angewendet.", "success");
  } catch (error) {
    setPlayerOffsetStatus(error.message, "error");
    showError(error.message);
  } finally {
    elements.playerOffsetApply.disabled = false;
    elements.playerPaymentExport.disabled = false;
  }
}

async function exportPlayerPaymentFiles() {
  elements.playerPaymentExport.disabled = true;
  elements.playerOffsetApply.disabled = true;
  setPlayerOffsetStatus("Bankdateien werden erstellt");
  try {
    await submitPlayerPaymentOffsets();
    const response = await fetch("/api/player-premium-payments/export", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({}),
    });
    const payload = await readResponse(response);
    if (payload.result) {
      renderPlayerPaymentResult(payload.result);
    }
    const transfer = payload.exports?.transfer || {};
    const debit = payload.exports?.debit || {};
    setPlayerOffsetStatus(
      `Erstellt: ${transfer.count || 0} Überweisungen, ` +
      `${debit.count || 0} Lastschriften.`,
      "success",
    );
  } catch (error) {
    setPlayerOffsetStatus(error.message, "error");
    showError(error.message);
  } finally {
    elements.playerPaymentExport.disabled = false;
    elements.playerOffsetApply.disabled = false;
  }
}

function paymentTeamSection(group) {
  const section = document.createElement("section");
  section.className = "payment-team-section";
  section.dataset.teamId = group.team_id || "";

  const heading = document.createElement("div");
  heading.className = "payment-team-heading";
  const title = document.createElement("h5");
  title.textContent = group.label || "Mannschaft";
  const count = document.createElement("span");
  const players = group.players || [];
  count.textContent = `${integerFormatter.format(players.length)} Spieler`;
  heading.append(title, count);
  section.append(heading);

  if (!players.length) {
    section.append(premiumEmptyMessage("Keine Prämien in dieser Mannschaft."));
    return section;
  }

  const frame = document.createElement("div");
  frame.className = "payment-review-frame";
  const table = document.createElement("table");
  table.className = "payment-review-table";
  const head = document.createElement("thead");
  const headingRow = document.createElement("tr");
  for (const label of [
    "Prämienliste",
    "DFBnet-Mitglied",
    "Übereinstimmung",
    "IBAN / BIC",
    "Validierung",
    "Verrechnung",
    "Finalbetrag",
    "Status",
    "Aktion",
  ]) {
    const cell = document.createElement("th");
    cell.textContent = label;
    headingRow.append(cell);
  }
  head.append(headingRow);
  const body = document.createElement("tbody");
  for (const player of players) {
    body.append(paymentPlayerRow(player));
  }
  table.append(head, body);
  frame.append(table);
  section.append(frame);
  return section;
}

function paymentPlayerRow(player) {
  const row = document.createElement("tr");
  const premiumName = document.createElement("th");
  premiumName.scope = "row";
  const name = document.createElement("strong");
  name.textContent = player.premium_name;
  const premium = document.createElement("small");
  const premiumTotal = Number(player.premium_total || 0);
  const combinedPremium = Number(player.combined_premium_total || premiumTotal);
  premium.textContent = currencyFormatter.format(premiumTotal);
  if (combinedPremium !== premiumTotal) {
    premium.textContent += ` · ${currencyFormatter.format(combinedPremium)} gesamt`;
  }
  premiumName.append(name, premium);

  const member = document.createElement("td");
  member.textContent = player.member_name || "Kein eindeutiger Treffer";

  const match = document.createElement("td");
  match.append(
    paymentStatusBadge(
      formatPaymentMatch(player.match_quality),
      paymentMatchClass(player.match_quality),
    ),
  );
  const score = document.createElement("small");
  score.textContent = player.match_score
    ? `${Math.round(Number(player.match_score) * 100)} %`
    : "";
  match.append(score);

  const bank = document.createElement("td");
  const iban = document.createElement("strong");
  iban.className = "is-monospace";
  iban.textContent = player.masked_iban || "Keine IBAN";
  const bic = document.createElement("small");
  bic.className = "is-monospace";
  bic.textContent = player.bic || "Keine BIC";
  bank.append(iban, bic);

  const validation = document.createElement("td");
  validation.append(
    paymentValidationLine("IBAN", player.iban_valid),
    paymentValidationLine("BIC", player.bic_valid),
    paymentAssignmentLine(player.iban_bic_assignment),
  );

  const offsets = document.createElement("td");
  const offsetItems = player.offsets || [];
  if (!offsetItems.length) {
    const empty = document.createElement("span");
    empty.className = "is-neutral";
    empty.textContent = "Keine Verrechnung";
    offsets.append(empty);
  } else {
    for (const offset of offsetItems) {
      const line = document.createElement("span");
      line.textContent =
        `${offset.label || "Gegenposition"}: ` +
        `-${currencyFormatter.format(Number(offset.amount || 0))}`;
      offsets.append(line);
    }
    const total = document.createElement("small");
    total.textContent =
      `Summe: -${currencyFormatter.format(Number(player.offset_total || 0))}`;
    offsets.append(total);
  }

  const final = document.createElement("td");
  const finalAmount = Number(player.final_amount || 0);
  const finalValue = document.createElement("strong");
  finalValue.textContent = currencyFormatter.format(finalAmount);
  final.append(finalValue);
  final.append(
    paymentStatusBadge(
      formatPaymentDirection(player.payment_direction),
      paymentDirectionClass(player.payment_direction),
    ),
  );

  const status = document.createElement("td");
  status.append(
    paymentStatusBadge(
      formatPaymentStatus(player.status),
      `is-${player.status || "nicht_gefunden"}`,
    ),
  );
  const source = document.createElement("small");
  source.textContent = player.payment_source === "manual"
    ? "Manuell eingetragen"
    : "Manuelle Bestätigung erforderlich";
  status.append(source);

  const action = document.createElement("td");
  const edit = document.createElement("button");
  edit.className = "payment-edit-action";
  edit.type = "button";
  edit.textContent = player.payment_source === "manual"
    ? "Manuelle Daten ersetzen"
    : "Zahlungsdaten eintragen";
  edit.disabled = !state.playerPaymentManualAvailable;
  edit.addEventListener("click", () => openPlayerPaymentDialog(player));
  action.append(edit);

  row.append(
    premiumName,
    member,
    match,
    bank,
    validation,
    offsets,
    final,
    status,
    action,
  );
  return row;
}

function openPlayerPaymentDialog(player) {
  state.editingPaymentPlayer = player.premium_name;
  elements.playerPaymentForm.reset();
  elements.playerPaymentDialogTitle.textContent =
    `Zahlungsdaten für ${player.premium_name}`;
  elements.playerPaymentIban.placeholder = player.masked_iban || "";
  elements.playerPaymentBic.placeholder = player.bic || "";
  elements.playerPaymentFormStatus.textContent = "";
  elements.playerPaymentFormStatus.className = "";
  elements.playerPaymentDialog.showModal();
  elements.playerPaymentAccountHolder.focus();
}

function closePlayerPaymentDialog() {
  state.editingPaymentPlayer = null;
  elements.playerPaymentDialog.close();
}

async function saveManualPlayerPayment(event) {
  event.preventDefault();
  const premiumName = state.editingPaymentPlayer;
  if (!premiumName) {
    return;
  }
  const submit = elements.playerPaymentForm.querySelector(
    "button[type='submit']",
  );
  submit.disabled = true;
  elements.playerPaymentFormStatus.textContent = "Wird gespeichert";
  elements.playerPaymentFormStatus.className = "is-saving";
  try {
    const response = await fetch(
      `/api/player-premium-payments/${encodeURIComponent(premiumName)}`,
      {
        method: "PATCH",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          account_holder: elements.playerPaymentAccountHolder.value,
          iban: elements.playerPaymentIban.value,
          bic: elements.playerPaymentBic.value,
        }),
      },
    );
    const payload = await readResponse(response);
    renderPlayerPaymentStatus(payload);
    elements.playerPaymentDialog.close();
    state.editingPaymentPlayer = null;
  } catch (error) {
    elements.playerPaymentFormStatus.textContent = error.message;
    elements.playerPaymentFormStatus.className = "is-error";
  } finally {
    submit.disabled = false;
  }
}

function paymentSummaryItem(label, value, className) {
  const item = document.createElement("div");
  item.className = `payment-summary-item ${className}`;
  const count = document.createElement("strong");
  count.textContent = typeof value === "number"
    ? integerFormatter.format(value)
    : String(value);
  const text = document.createElement("span");
  text.textContent = label;
  item.append(count, text);
  return item;
}

function paymentValidationLine(label, valid) {
  const line = document.createElement("span");
  line.className = valid ? "is-valid" : "is-invalid";
  line.textContent = `${label}: ${valid ? "gültig" : "ungültig"}`;
  return line;
}

function paymentAssignmentLine(value) {
  const labels = {
    plausibel: "IBAN/BIC: plausibel",
    widerspruechlich: "IBAN/BIC: widersprüchlich",
    nicht_geprueft: "IBAN/BIC: nicht geprüft",
  };
  const line = document.createElement("span");
  line.className = value === "widerspruechlich"
    ? "is-invalid"
    : "is-neutral";
  line.textContent = labels[value] || labels.nicht_geprueft;
  return line;
}

function paymentStatusBadge(label, className) {
  const badge = document.createElement("span");
  badge.className = `payment-review-badge ${className}`;
  badge.textContent = label;
  return badge;
}

function formatOffsetAssignment(value) {
  const labels = {
    auto: "Automatisch",
    manual: "Manuell",
    unassigned: "Nicht zugeordnet",
  };
  return labels[value] || labels.unassigned;
}

function offsetAssignmentClass(value) {
  if (value === "auto") {
    return "is-valid";
  }
  if (value === "manual") {
    return "is-review";
  }
  return "is-missing";
}

function formatPaymentDirection(value) {
  const labels = {
    transfer: "Überweisung",
    debit: "Lastschrift",
    balanced: "Ausgeglichen",
  };
  return labels[value] || labels.balanced;
}

function paymentDirectionClass(value) {
  if (value === "transfer") {
    return "is-valid";
  }
  if (value === "debit") {
    return "is-review";
  }
  return "is-neutral";
}

function paymentMatchClass(value) {
  if (value === "exakt" || value === "normalisiert") {
    return "is-valid";
  }
  if (value === "ähnlich" || value === "mehrdeutig") {
    return "is-review";
  }
  return "is-missing";
}

function formatPaymentMatch(value) {
  const labels = {
    exakt: "Exakt",
    normalisiert: "Normalisiert",
    "ähnlich": "Ähnlich",
    mehrdeutig: "Mehrdeutig",
    kein_treffer: "Kein Treffer",
  };
  return labels[value] || value || "Kein Treffer";
}

function formatPaymentStatus(value) {
  const labels = {
    eindeutig_gefunden: "Eindeutig gefunden",
    manuell_pruefen: "Manuell prüfen",
    nicht_gefunden: "Nicht gefunden",
  };
  return labels[value] || value || "Nicht gefunden";
}

async function loadTransactions() {
  if (state.transactionRequest) {
    state.transactionRequest.abort();
  }
  state.transactionRequest = new AbortController();
  setTransactionLoading(true);
  const parameters = new URLSearchParams({
    search: state.search,
    sort: state.sort,
    direction: state.direction,
    date_from: state.dateFrom,
    date_to: state.dateTo,
    hide_completed_vorgaenge: String(
      state.hideCompletedVorgaengeTransactions,
    ),
    unclassified_only: String(state.unclassifiedTransactionsOnly),
  });
  try {
    const response = await fetch(`/api/transactions?${parameters}`, {
      signal: state.transactionRequest.signal,
    });
    const payload = await readResponse(response);
    state.hideCompletedVorgaengeTransactions = Boolean(
      payload.hide_completed_vorgaenge,
    );
    state.unclassifiedTransactionsOnly = Boolean(payload.unclassified_only);
    elements.transactionHideCompletedVorgaenge.checked =
      state.hideCompletedVorgaengeTransactions;
    renderTransactions(payload.transactions);
    elements.transactionCount.textContent = integerFormatter.format(payload.count);
    elements.transactionCountLabel.textContent =
      payload.count === 1 ? "Transaktion" : "Transaktionen";
    renderBalances(payload.balances);
  } catch (error) {
    if (error.name !== "AbortError") {
      showError(error.message);
      renderTransactions([]);
    }
  } finally {
    setTransactionLoading(false);
  }
}

function renderTransactions(transactions) {
  elements.transactionRows.replaceChildren();
  for (const transaction of transactions) {
    const row = document.createElement("tr");
    row.tabIndex = 0;
    row.dataset.id = transaction.transaktions_id;
    row.setAttribute(
      "aria-label",
      `Details für Transaktion vom ${formatDate(transaction.datum)}`,
    );
    row.addEventListener(
      "click",
      () => openTransaction(transaction.transaktions_id),
    );
    row.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openTransaction(transaction.transaktions_id);
      }
    });

    row.append(
      tableCell(formatDate(transaction.datum), "date-cell"),
      tableCell(transaction.kontoname, "account-cell"),
      tableCell(transaction.zahlungsbeteiligter, "counterparty-cell"),
      purposeCell(transaction.verwendungszweck),
      transactionVorgangCell(transaction),
      amountCell(transaction.betrag),
      balanceCell(transaction.kontostand_konto),
    );
    elements.transactionRows.append(row);
  }
  const empty = transactions.length === 0;
  elements.transactionEmpty.hidden = !empty;
  elements.transactionTable.hidden = empty;
}

function tableCell(value, className = "") {
  const cell = document.createElement("td");
  cell.className = className;
  cell.textContent = value || "";
  cell.title = value || "";
  return cell;
}

function transactionVorgangCell(transaction) {
  const cell = document.createElement("td");
  cell.className = "transaction-vorgang-cell";
  const count = Number(transaction.vorgaenge_count || 0);
  const completedCount = Number(transaction.completed_vorgaenge_count || 0);
  if (!count) {
    const empty = document.createElement("span");
    empty.className = "is-unavailable";
    empty.textContent = "Kein Vorgang";
    cell.append(empty);
    return cell;
  }

  const linked = document.createElement("span");
  linked.className = "status-badge is-open";
  linked.textContent = count === 1 ? "Vorgang" : `${count} Vorgänge`;
  linked.title = `${count} verknüpfte Vorgänge`;
  cell.append(linked);

  if (completedCount) {
    const completed = document.createElement("span");
    completed.className = "status-badge is-complete";
    completed.textContent =
      completedCount === count
        ? "Abgeschlossen"
        : `${completedCount} abgeschlossen`;
    completed.title = `${completedCount} von ${count} Vorgängen abgeschlossen`;
    cell.append(completed);
  }
  return cell;
}

function purposeCell(value) {
  const cell = document.createElement("td");
  const text = document.createElement("span");
  text.className = "purpose-text";
  text.textContent = value || "";
  text.title = value || "";
  cell.append(text);
  return cell;
}

function amountCell(value) {
  const cell = document.createElement("td");
  cell.className = "amount-column";
  cell.append(amountBadge(value));
  return cell;
}

function balanceCell(value) {
  const cell = document.createElement("td");
  cell.className = "amount-column balance-column";
  if (value === null || value === undefined || value === "") {
    cell.classList.add("is-unavailable");
    cell.textContent = "Nicht verfügbar";
    return cell;
  }
  cell.textContent = currencyFormatter.format(Number(value));
  return cell;
}

function setTransactionLoading(loading) {
  elements.transactionLoading.hidden = !loading;
  if (loading) {
    elements.transactionTable.hidden = true;
    elements.transactionEmpty.hidden = true;
  }
}

function updateSortIndicators() {
  elements.sortButtons.forEach((button) => {
    const header = button.closest("th");
    if (button.dataset.sort === state.sort) {
      header.setAttribute(
        "aria-sort",
        state.direction === "asc" ? "ascending" : "descending",
      );
    } else {
      header.removeAttribute("aria-sort");
    }
  });
}

async function loadVorgaenge() {
  if (state.vorgangRequest) {
    state.vorgangRequest.abort();
  }
  state.vorgangRequest = new AbortController();
  setVorgangLoading(true);
  const parameters = new URLSearchParams({
    search: state.vorgangSearch,
    hide_completed: String(state.vorgangHideCompleted),
  });
  try {
    const response = await fetch(`/api/vorgaenge?${parameters}`, {
      signal: state.vorgangRequest.signal,
    });
    const payload = await readResponse(response);
    renderVorgaenge(payload.vorgaenge);
    elements.vorgangCount.textContent = integerFormatter.format(payload.count);
    elements.vorgangCountLabel.textContent =
      payload.count === 1 ? "Vorgang" : "Vorgänge";
    state.vorgaengeLoaded = true;
  } catch (error) {
    if (error.name !== "AbortError") {
      showError(error.message);
      renderVorgaenge([]);
    }
  } finally {
    setVorgangLoading(false);
  }
}

async function loadVorgangTypes(force = false) {
  if (state.vorgangTypesLoaded && !force) {
    return state.vorgangTypes;
  }
  const response = await fetch("/api/vorgaenge/types");
  const payload = await readResponse(response);
  state.vorgangTypes = payload.types || [];
  state.vorgangTypesLoaded = true;
  return state.vorgangTypes;
}

async function loadLinkCandidates(force = false) {
  if (state.linkCandidatesLoaded && !force) {
    return state.linkCandidates;
  }
  const response = await fetch("/api/vorgaenge/link-candidates");
  const payload = await readResponse(response);
  state.linkCandidates = payload.candidates || {};
  state.linkCandidatesLoaded = true;
  return state.linkCandidates;
}

function renderVorgaenge(vorgaenge) {
  const listedTypes = vorgaenge
    .map((vorgang) => String(vorgang.vorgangstyp || "").trim())
    .filter(Boolean);
  if (listedTypes.length) {
    state.vorgangTypes = [...new Set([...state.vorgangTypes, ...listedTypes])]
      .sort((left, right) => left.localeCompare(right, "de"));
  }
  elements.vorgangRows.replaceChildren();
  for (const vorgang of vorgaenge) {
    const row = document.createElement("tr");
    row.tabIndex = 0;
    row.dataset.id = vorgang.vorgangs_id;
    row.setAttribute("aria-label", `Details für Vorgang ${vorgang.vorgangs_id}`);
    row.addEventListener("click", () => openVorgang(vorgang.vorgangs_id));
    row.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openVorgang(vorgang.vorgangs_id);
      }
    });
    row.append(
      tableCell(formatDate(vorgang.letztes_datum), "date-cell"),
      tableCell(vorgang.titel || vorgang.bezug, "counterparty-cell"),
      tableCell(vorgang.vorgangstyp, "account-cell"),
      statusCell(vorgang.status),
      tableCell(vorgang.bezug, "counterparty-cell"),
      tableCell(
        integerFormatter.format(vorgang.anzahl_transaktionen),
        "amount-column",
      ),
      tableCell(
        integerFormatter.format(
          Number(vorgang.anzahl_mails || 0) +
          Number(vorgang.anzahl_todos || 0) +
          Number(vorgang.anzahl_belege || 0) +
          Number(vorgang.anzahl_termine || 0),
        ),
        "amount-column",
      ),
      vorgangActionCell(vorgang),
    );
    elements.vorgangRows.append(row);
  }
  const empty = vorgaenge.length === 0;
  elements.vorgangEmpty.hidden = !empty;
  elements.vorgangTable.hidden = empty;
}

function vorgangActionCell(vorgang) {
  const cell = document.createElement("td");
  const button = mailElement(
    "button",
    "row-delete-action danger-action",
    "Löschen",
  );
  button.type = "button";
  button.title = "Vorgang löschen";
  button.addEventListener("click", (event) => {
    event.stopPropagation();
    deleteVorgang(vorgang, button);
  });
  cell.append(button);
  return cell;
}

function statusCell(value) {
  const cell = document.createElement("td");
  cell.append(statusBadge(value));
  return cell;
}

function statusBadge(value) {
  const badge = document.createElement("span");
  badge.className =
    `status-badge ${value === "abgeschlossen" ? "is-complete" : "is-open"}`;
  badge.textContent = formatStatus(value);
  return badge;
}

function setVorgangLoading(loading) {
  elements.vorgangLoading.hidden = !loading;
  if (loading) {
    elements.vorgangTable.hidden = true;
    elements.vorgangEmpty.hidden = true;
  }
}

async function openVorgangCreateDialog(source = null) {
  elements.dialog.classList.add("is-vorgang");
  elements.dialog.classList.remove("has-rule-workspace");
  delete elements.dialog.dataset.vorgangId;
  delete elements.dialog.dataset.vorgangTransactionCount;
  elements.detailEyebrow.textContent = source
    ? "Vorgang erstellen"
    : "Neuer Vorgang";
  elements.detailTitle.textContent = source?.title || "Neuer Vorgang";
  elements.detailSubtitle.textContent = source
    ? "Vorschläge prüfen und bestätigen"
    : "Manuelle Erfassung";
  elements.detailContent.replaceChildren(createLoadingBlock());
  elements.dialog.showModal();
  try {
    const [suggestions, , candidates] = await Promise.all([
      source ? loadVorgangSuggestions(source.type, source.id) : Promise.resolve(null),
      loadVorgangTypes(),
      loadLinkCandidates(),
    ]);
    renderVorgangCreateForm(source, mergeLinkCandidates(suggestions, candidates));
  } catch (error) {
    renderVorgangCreateForm(source, null);
    showError(error.message);
  }
}

async function loadVorgangSuggestions(sourceType, sourceId) {
  const response = await fetch("/api/vorgaenge/suggestions", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({source_type: sourceType, source_id: sourceId}),
  });
  return readResponse(response);
}

function mergeLinkCandidates(suggestionsPayload, candidates) {
  if (!suggestionsPayload) {
    return {suggestions: {}, candidates: candidates || {}};
  }
  return {
    ...suggestionsPayload,
    candidates: {
      ...(candidates || {}),
      ...(suggestionsPayload.candidates || {}),
    },
  };
}

function linkItems(payload, key) {
  const suggestions = payload?.suggestions?.[key] || [];
  const candidates = payload?.candidates?.[key] || [];
  const byId = new Map();
  for (const item of candidates) {
    if (item?.id) {
      byId.set(String(item.id), {...item, source: "candidate"});
    }
  }
  for (const item of suggestions) {
    if (item?.id) {
      byId.set(String(item.id), {...byId.get(String(item.id)), ...item, source: "suggestion"});
    }
  }
  return [...byId.values()].sort(compareSuggestionItems);
}

function compareSuggestionItems(left, right) {
  const leftPriority = suggestionPriority(left);
  const rightPriority = suggestionPriority(right);
  if (leftPriority !== rightPriority) {
    return rightPriority - leftPriority;
  }
  const scoreDelta = Number(right.score || 0) - Number(left.score || 0);
  if (scoreDelta !== 0) {
    return scoreDelta;
  }
  return String(right.date || "").localeCompare(String(left.date || ""));
}

function suggestionPriority(item) {
  if (item?.selected) {
    return 5;
  }
  if (item?.relation === "conversation") {
    return 4;
  }
  if (Number(item?.score || 0) >= 0.45) {
    return 3;
  }
  if (item?.source === "suggestion") {
    return 2;
  }
  return 1;
}

function entityTypeForSuggestionField(fieldName) {
  return {
    transaction_ids: "transaction",
    mail_ids: "mail",
    todo_ids: "todo",
    beleg_ids: "beleg",
    termin_ids: "termin",
  }[fieldName] || "";
}

function renderVorgangCreateForm(source, suggestionsPayload) {
  elements.detailContent.replaceChildren();
  const form = mailElement("form", "vorgang-create-form");
  form.dataset.vorgangCreateForm = "";
  const fieldset = mailElement("section", "detail-section");
  fieldset.append(mailElement("h3", "", "Vorgangsdaten"));
  const grid = mailElement("div", "detail-grid");
  grid.append(
    formTextField("Titel", "title", source?.title || "", true),
    formVorgangTypeField("vorgangstyp", source?.vorgangstyp || ""),
    formTextField(
      "Beschreibung",
      "description",
      source?.description || "",
      false,
      true,
    ),
  );
  const completed = mailElement("label", "checkbox-field is-wide");
  const completedInput = document.createElement("input");
  completedInput.type = "checkbox";
  completedInput.name = "completed";
  completed.append(completedInput, mailElement("span", "", "Direkt abschließen"));
  grid.append(completed);
  fieldset.append(grid);
  form.append(fieldset);

  const links = sourceLinkPayload(source);
  form.append(createSuggestionSection("Transaktionen", "transaction_ids", links.transaction_ids, linkItems(suggestionsPayload, "transactions")));
  form.append(createSuggestionSection("Mails", "mail_ids", links.mail_ids, linkItems(suggestionsPayload, "mails")));
  form.append(createSuggestionSection("To-Dos", "todo_ids", links.todo_ids, linkItems(suggestionsPayload, "todos"), "todo"));
  form.append(createSuggestionSection("Dokumente", "beleg_ids", links.beleg_ids, linkItems(suggestionsPayload, "belege")));
  form.append(createSuggestionSection("Termine", "termin_ids", links.termin_ids, linkItems(suggestionsPayload, "termine"), "termin"));

  const formError = mailElement("p", "form-error");
  formError.hidden = true;
  const actions = mailElement("div", "vorgang-form-actions");
  const submit = mailElement("button", "primary-action", "Vorgang erstellen");
  submit.type = "submit";
  const status = mailElement("span", "save-state");
  actions.append(submit, status);
  form.append(formError, actions);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    submit.disabled = true;
    formError.hidden = true;
    formError.textContent = "";
    status.className = "save-state is-saving";
    status.textContent = "Vorgang wird erstellt";
    try {
      const response = await fetch("/api/vorgaenge", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(readVorgangForm(form)),
      });
      const payload = await readResponse(response);
      rememberVorgangType(form.elements.vorgangstyp.value);
      state.vorgaengeLoaded = false;
      state.todosLoaded = false;
      state.termineLoaded = false;
      await Promise.all([loadOverview(), loadVorgaenge()]);
      elements.dialog.close();
      activateTab("vorgaenge");
      await openVorgang(payload.vorgang.vorgangs_id);
    } catch (error) {
      submit.disabled = false;
      status.className = "save-state is-error";
      status.textContent = "Erstellen fehlgeschlagen";
      formError.textContent = error.message;
      formError.hidden = false;
      showError(error.message);
    }
  });
  elements.detailContent.append(form);
}

function formTextField(labelText, name, value = "", required = false, multiline = false) {
  const label = mailElement("label", multiline ? "is-wide" : "");
  label.append(mailElement("span", "detail-label", labelText));
  const input = document.createElement(multiline ? "textarea" : "input");
  input.name = name;
  input.maxLength = name === "title" ? 300 : 10000;
  input.required = required;
  if (multiline) {
    input.rows = 4;
  } else {
    input.type = "text";
  }
  input.value = value || "";
  label.append(input);
  return label;
}

function formVorgangTypeField(name, value = "") {
  const label = mailElement("label");
  label.append(mailElement("span", "detail-label", "Vorgangstyp"));
  const input = document.createElement("input");
  input.name = name;
  input.type = "text";
  input.maxLength = 2000;
  input.autocomplete = "off";
  input.value = value || "";
  const datalist = document.createElement("datalist");
  datalist.id = `vorgang-types-${ruleDatalistCounter += 1}`;
  for (const type of state.vorgangTypes || []) {
    const option = document.createElement("option");
    option.value = type;
    datalist.append(option);
  }
  input.setAttribute("list", datalist.id);
  label.append(input, datalist);
  return label;
}

function rememberVorgangType(value) {
  const type = String(value || "").trim();
  if (!type || state.vorgangTypes.includes(type)) {
    return;
  }
  state.vorgangTypes = [...state.vorgangTypes, type]
    .sort((left, right) => left.localeCompare(right, "de"));
}

function sourceLinkPayload(source) {
  const links = {
    transaction_ids: [],
    mail_ids: [],
    todo_ids: [],
    beleg_ids: [],
    termin_ids: [],
  };
  if (!source) {
    return links;
  }
  const mapping = {
    transaction: "transaction_ids",
    mail: "mail_ids",
    todo: "todo_ids",
    beleg: "beleg_ids",
    termin: "termin_ids",
  };
  const field = mapping[source.type];
  if (field) {
    links[field] = [source.id];
  }
  return links;
}

function createSuggestionSection(
  title,
  fieldName,
  selectedIds,
  suggestions,
  createTarget = "",
) {
  const section = mailElement("section", "detail-section suggestion-section");
  section.dataset.suggestionField = fieldName;
  const heading = mailElement("div", "suggestion-heading");
  heading.append(mailElement("h3", "", title));
  if (createTarget) {
    const createButton = mailElement(
      "button",
      "secondary-action suggestion-create-action",
      createTarget === "todo" ? "Neues To-Do" : "Neuer Termin",
    );
    createButton.type = "button";
    createButton.addEventListener("click", () => {
      if (elements.dialog.open) {
        elements.dialog.close();
      }
      activateTab(createTarget === "todo" ? "todos" : "termine");
      if (createTarget === "todo") {
        resetTodoForm();
        elements.todoTitle.focus();
      } else {
        resetTerminForm();
        elements.terminTitle.focus();
      }
    });
    heading.append(createButton);
  }
  section.append(heading);
  const searchLabel = mailElement("label", "suggestion-search");
  searchLabel.append(
    mailElement("span", "", "Suchen"),
  );
  const search = document.createElement("input");
  search.type = "search";
  search.autocomplete = "off";
  search.placeholder = `${title} durchsuchen`;
  searchLabel.append(search);
  const list = mailElement("div", "suggestion-list");
  const selected = new Set(selectedIds || []);
  const suggestionsById = new Map(
    suggestions
      .filter((item) => item?.id)
      .map((item) => [String(item.id), item]),
  );
  const rows = [
    ...(selectedIds || []).map((id) => ({
      ...(suggestionsById.get(String(id)) || {}),
      id,
      label: suggestionsById.get(String(id))?.label || id,
      reason: "Quelle",
      score: 1,
      selected: true,
    })),
    ...suggestions.filter((item) => !selected.has(item.id)),
  ].sort(compareSuggestionItems);
  if (!rows.length) {
    list.append(
      mailElement(
        "p",
        "suggestion-empty",
        "Keine vorhandenen Einträge gefunden.",
      ),
    );
  }
  const entityType = entityTypeForSuggestionField(fieldName);
  for (const item of rows) {
    const row = mailElement("div", "suggestion-row");
    row.classList.toggle(
      "is-suggested",
      item.source === "suggestion" || item.relation === "conversation",
    );
    row.dataset.searchText = [
      item.label,
      item.id,
      item.reason,
      item.date,
      item.amount,
      item.status,
      item.category,
      item.sender,
      item.preview,
      ...(item.classification_missing || []),
    ].filter(Boolean).join(" ").toLocaleLowerCase("de-DE");
    const label = mailElement("label", "suggestion-choice");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = item.id;
    checkbox.checked = Boolean(item.selected);
    const text = mailElement("span");
    text.append(
      mailElement("strong", "", item.label || item.id),
      mailElement(
        "small",
        "",
        [
          item.reason,
          item.sender,
          item.date ? formatDateTimeOrDate(item.date) : "",
          item.amount ? currencyFormatter.format(Number(item.amount)) : "",
          item.status,
          item.category,
          transactionClassificationSummary(item),
        ].filter(Boolean).join(" · "),
      ),
    );
    label.append(checkbox, text);
    row.append(label);
    if (entityType && item.id) {
      const actions = mailElement("div", "document-actions");
      const openButton = mailElement(
        "button",
        "suggestion-open-action",
        entityType === "beleg" ? "Katalogeintrag öffnen" : "Öffnen",
      );
      openButton.type = "button";
      openButton.dataset.openEntityType = entityType;
      openButton.dataset.openEntityId = item.id;
      openButton.addEventListener("click", () => {
        openEntityPreview(entityType, item.id);
      });
      actions.append(openButton);
      if (entityType === "beleg") {
        actions.append(originalDocumentLink(item.id));
      }
      row.append(actions);
    }
    list.append(row);
  }
  search.addEventListener("input", () => {
    const query = search.value.trim().toLocaleLowerCase("de-DE");
    for (const row of list.querySelectorAll(".suggestion-row")) {
      row.hidden = Boolean(query) && !row.dataset.searchText.includes(query);
    }
  });
  section.append(searchLabel, list);
  return section;
}

function transactionClassificationSummary(item) {
  if (!item || !("classification_complete" in item)) {
    return "";
  }
  if (item.classification_complete) {
    const values = Object.values(item.classification || {})
      .filter(Boolean)
      .join(" / ");
    return values
      ? `Vollständig klassifiziert: ${values}`
      : "Vollständig klassifiziert";
  }
  const missing = item.classification_missing || [];
  return missing.length
    ? `Unvollständig klassifiziert, fehlt: ${missing.join(", ")}`
    : "Unvollständig klassifiziert";
}

async function openEntityPreview(type, id) {
  state.entityPreviewAttachments = [];
  delete elements.entityPreviewContent.dataset.mailPreviewId;
  elements.entityPreviewEyebrow.textContent = entityPreviewLabel(type);
  elements.entityPreviewTitle.textContent = "Details werden geladen";
  elements.entityPreviewSubtitle.textContent = "";
  elements.entityPreviewContent.replaceChildren(createLoadingBlock());
  if (!elements.entityDialog.open) {
    elements.entityDialog.showModal();
  }
  try {
    if (type === "transaction") {
      await renderTransactionPreview(id);
    } else if (type === "mail") {
      await renderMailEntityPreview(id);
    } else if (type === "todo") {
      await renderTodoEntityPreview(id);
    } else if (type === "termin") {
      await renderTerminEntityPreview(id);
    } else if (type === "beleg") {
      await renderBelegEntityPreview(id);
    } else {
      throw new Error("Unbekannter Entitätstyp.");
    }
  } catch (error) {
    elements.entityPreviewContent.replaceChildren();
    showError(error.message);
  }
}

function entityPreviewLabel(type) {
  return {
    transaction: "Transaktion",
    mail: "Mail",
    todo: "To-Do",
    beleg: "Dokument",
    termin: "Termin",
  }[type] || "Entität";
}

async function renderTransactionPreview(transaktionsId) {
  const [transactionResponse, splitsResponse, optionsResponse] = await Promise.all([
    fetch(`/api/transactions/${encodeURIComponent(transaktionsId)}`),
    fetch(`/api/transactions/${encodeURIComponent(transaktionsId)}/splits`),
    fetch("/api/classification-options"),
  ]);
  const [payload, splitsPayload, options] = await Promise.all([
    readResponse(transactionResponse),
    readResponse(splitsResponse),
    readResponse(optionsResponse),
  ]);
  const transaction = payload.transaction;
  transaction.splits = splitsPayload.splits || [];
  transaction.zulaessige_vorgaenge = splitsPayload.zulaessige_vorgaenge || [];
  state.classificationOptions = options;
  elements.entityPreviewTitle.textContent =
    transaction.zahlungsbeteiligter || transaction.verwendungszweck || transaktionsId;
  elements.entityPreviewSubtitle.textContent =
    `${formatDate(transaction.datum)} · ${transaction.kontoname || ""}`;
  elements.entityPreviewContent.replaceChildren();
  renderTransactionContent(transaction, elements.entityPreviewContent);
}

async function renderMailEntityPreview(entryId) {
  const response = await fetch(`/api/mail/${encodeURIComponent(entryId)}`);
  const payload = await readResponse(response);
  const detail = payload.message;
  state.entityPreviewAttachments = detail.attachments || [];
  state.selectedMailAttachment =
    detail.attachments?.[0]?.attachmentIndex || null;
  elements.entityPreviewTitle.textContent = detail.subject || "(ohne Betreff)";
  elements.entityPreviewSubtitle.textContent = [
    [detail.fromName, detail.fromAddress].filter(Boolean).join(" · "),
    formatDateTime(detail.receivedDateTime),
    detail.isConversation
      ? `Mailverlauf: ${detail.conversationMessageCount || 1}`
      : "",
  ].filter(Boolean).join(" · ");
  const layout = mailElement("div", "mail-reading-layout");
  const bodySection = mailElement("section", "mail-body-pane");
  bodySection.append(
    mailElement("h4", "", "Mail"),
    mailElement("pre", "mail-body-text", detail.body || "(kein Textinhalt)"),
  );
  layout.append(bodySection, renderMailAttachmentPane({...detail, id: entryId}));
  elements.entityPreviewContent.dataset.mailPreviewId = entryId;
  elements.entityPreviewContent.replaceChildren(layout);
  applyMailZoom();
}

async function renderTodoEntityPreview(todoId, assignmentStatus = "") {
  const [todoResponse, vorgangResponse] = await Promise.all([
    fetch(`/api/todos/${encodeURIComponent(todoId)}`),
    fetch("/api/vorgaenge"),
  ]);
  const [payload, vorgangPayload] = await Promise.all([
    readResponse(todoResponse),
    readResponse(vorgangResponse),
  ]);
  const todo = payload.todo;
  elements.entityPreviewTitle.textContent = todo.title || todo.todo_id;
  elements.entityPreviewSubtitle.textContent = [
    todo.priority ? todoPriorityLabel(todo.priority) : "",
    todo.due_date ? `Fällig: ${formatDate(todo.due_date)}` : "",
    todo.completed ? "Abgeschlossen" : "Offen",
  ].filter(Boolean).join(" · ");
  elements.entityPreviewContent.replaceChildren(
    renderTodoEntityForm(todo, vorgangPayload.vorgaenge || []),
  );
  if (assignmentStatus) {
    setAssignmentStatus(
      elements.entityPreviewContent.querySelector(".save-state"),
      "saved",
      assignmentStatus,
    );
  }
}

function renderTodoEntityForm(todo, vorgaenge) {
  const form = mailElement("form", "entity-edit-form");
  form.append(
    formTextField("Titel", "title", todo.title || "", true),
    formTextField("Beschreibung", "description", todo.description || "", false, true),
    compactInputField("Fällig am", "due_date", todo.due_date || "", "date"),
    selectField("Priorität", "priority", {
      niedrig: "Niedrig",
      normal: "Normal",
      hoch: "Hoch",
    }, todo.priority || "normal"),
  );
  const completed = mailElement("label", "checkbox-field is-wide");
  const completedInput = document.createElement("input");
  completedInput.type = "checkbox";
  completedInput.name = "completed";
  completedInput.checked = Boolean(todo.completed);
  completed.append(completedInput, mailElement("span", "", "Abgeschlossen"));
  form.append(completed, entityVorgangSelect(vorgaenge, todo.vorgangs_ids || []));
  const actions = entityFormActions("Änderungen und Zuordnung bestätigen");
  form.append(actions.container);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const selectedIds = [...form.elements.vorgangs_ids.selectedOptions]
      .map((option) => option.value);
    await submitVorgangAssignment({
      form,
      submit: actions.submit,
      status: actions.status,
      selectedId: selectedIds[0] || "",
      request: () => persistTodo({
        title: form.elements.title.value,
        description: form.elements.description.value,
        due_date: form.elements.due_date.value,
        priority: form.elements.priority.value,
        completed: form.elements.completed.checked,
        vorgangs_ids: selectedIds,
      }, todo.todo_id),
      onSaved: async () => {
        state.todosLoaded = false;
        state.vorgaengeLoaded = false;
        await Promise.all([loadOverview(), loadTodos().catch(() => null)]);
        await renderTodoEntityPreview(todo.todo_id, "Zuordnung gespeichert");
      },
    });
  });
  return form;
}

async function renderTerminEntityPreview(terminId, assignmentStatus = "") {
  const [terminResponse, vorgangResponse] = await Promise.all([
    fetch(`/api/termine/${encodeURIComponent(terminId)}`),
    fetch("/api/vorgaenge"),
  ]);
  const [payload, vorgangPayload] = await Promise.all([
    readResponse(terminResponse),
    readResponse(vorgangResponse),
  ]);
  const termin = payload.termin;
  elements.entityPreviewTitle.textContent = termin.title || termin.termin_id;
  elements.entityPreviewSubtitle.textContent = [
    formatDateTime(termin.starts_at),
    termin.location,
    terminStatusLabel(termin.status),
  ].filter(Boolean).join(" · ");
  elements.entityPreviewContent.replaceChildren(
    renderTerminEntityForm(termin, vorgangPayload.vorgaenge || []),
  );
  if (assignmentStatus) {
    setAssignmentStatus(
      elements.entityPreviewContent.querySelector(".save-state"),
      "saved",
      assignmentStatus,
    );
  }
}

function renderTerminEntityForm(termin, vorgaenge) {
  const form = mailElement("form", "entity-edit-form");
  form.append(
    formTextField("Titel", "title", termin.title || "", true),
    formTextField("Beschreibung", "description", termin.description || "", false, true),
    compactInputField(
      "Beginn",
      "starts_at",
      apiDateTimeToLocalInput(termin.starts_at || ""),
      "datetime-local",
    ),
    compactInputField(
      "Ende",
      "ends_at",
      apiDateTimeToLocalInput(termin.ends_at || ""),
      "datetime-local",
    ),
    compactInputField("Ort", "location", termin.location || ""),
    selectField("Status", "status", {
      geplant: "Geplant",
      abgeschlossen: "Abgeschlossen",
      abgesagt: "Abgesagt",
    }, termin.status || "geplant"),
    entityVorgangSelect(vorgaenge, termin.vorgangs_ids || []),
  );
  const actions = entityFormActions("Änderungen und Zuordnung bestätigen");
  form.append(actions.container);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const selectedIds = [...form.elements.vorgangs_ids.selectedOptions]
      .map((option) => option.value);
    await submitVorgangAssignment({
      form,
      submit: actions.submit,
      status: actions.status,
      selectedId: selectedIds[0] || "",
      request: async () => {
        const response = await fetch(
        `/api/termine/${encodeURIComponent(termin.termin_id)}`,
        {
          method: "PATCH",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({
            title: form.elements.title.value,
            description: form.elements.description.value,
            starts_at: localDateTimeToApiValue(form.elements.starts_at.value),
            ends_at: localDateTimeToApiValue(form.elements.ends_at.value),
            location: form.elements.location.value,
            status: form.elements.status.value,
            vorgangs_ids: selectedIds,
          }),
        },
        );
        await readResponse(response);
      },
      onSaved: async () => {
        state.termineLoaded = false;
        state.vorgaengeLoaded = false;
        await Promise.all([loadOverview(), loadTermine().catch(() => null)]);
        await renderTerminEntityPreview(termin.termin_id, "Zuordnung gespeichert");
      },
    });
  });
  return form;
}

async function renderBelegEntityPreview(belegId, assignmentStatus = "") {
  const [response, vorgangResponse] = await Promise.all([
    fetch(`/api/belege/${encodeURIComponent(belegId)}`),
    fetch("/api/vorgaenge"),
  ]);
  const [payload, vorgangPayload] = await Promise.all([
    readResponse(response),
    readResponse(vorgangResponse),
  ]);
  const beleg = payload.beleg;
  elements.entityPreviewTitle.textContent = beleg.filename || beleg.dateiname || beleg.beleg_id;
  elements.entityPreviewSubtitle.textContent = [
    beleg.category || beleg.kategorie,
    beleg.document_date ? formatDate(beleg.document_date) : "",
    beleg.amount ? currencyFormatter.format(Number(beleg.amount)) : "",
  ].filter(Boolean).join(" · ");
  elements.entityPreviewContent.replaceChildren();
  appendDetailSection("Dokument", [
    detailField("Beleg-ID", beleg.beleg_id, true, true),
    detailField("Dateiname", beleg.filename || beleg.dateiname, true),
    detailField("Kategorie", beleg.category || beleg.kategorie),
    detailField("Dokumentdatum", formatDate(beleg.document_date || beleg.dokumentdatum)),
    detailField("Betrag", beleg.amount || beleg.betrag),
    detailField("Aussteller", beleg.issuer || beleg.aussteller),
    detailField("Empfänger", beleg.recipient || beleg.empfaenger),
    detailField("Beschreibung", beleg.description || beleg.beschreibung, true),
    detailField("Pfad", beleg.path || beleg.dateipfad, true, true),
    detailField("Vorgangs-IDs", joinValues(beleg.vorgangs_ids), true, true),
    belegActionField(beleg),
  ], elements.entityPreviewContent);
  elements.entityPreviewContent.append(createStandaloneVorgangAssignment({
    entityLabel: "Dokument",
    entityId: beleg.beleg_id,
    endpoint: `/api/belege/${encodeURIComponent(beleg.beleg_id)}/vorgaenge`,
    vorgaenge: (vorgangPayload.vorgaenge || []).filter(
      (vorgang) => !(beleg.vorgangs_ids || []).includes(vorgang.vorgangs_id),
    ),
    selectedIds: beleg.vorgangs_ids || [],
    onSaved: () => renderBelegEntityPreview(beleg.beleg_id, "Zuordnung gespeichert"),
  }));
  if (assignmentStatus) {
    const status = elements.entityPreviewContent.querySelector(
      "[data-assignment-entity] .save-state",
    );
    setAssignmentStatus(status, "saved", assignmentStatus);
  }
}

function createStandaloneVorgangAssignment({
  entityLabel, entityId, endpoint, vorgaenge, selectedIds, onSaved,
}) {
  const section = mailElement("section", "detail-section assignment-panel");
  section.dataset.assignmentEntity = entityId;
  section.append(mailElement("h3", "", `${entityLabel} einem Vorgang zuordnen`));
  const form = mailElement("form", "mail-vorgang-form");
  form.append(entityVorgangSelect(vorgaenge, selectedIds, true));
  const actions = entityFormActions("Zuordnung bestätigen");
  form.append(actions.container);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const selected = form.elements.vorgangs_ids.value;
    await submitVorgangAssignment({
      form,
      submit: actions.submit,
      status: actions.status,
      selectedId: selected,
      request: async () => {
        const response = await fetch(endpoint, {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({vorgangs_id: selected}),
        });
        await readResponse(response);
        state.vorgaengeLoaded = false;
      },
      onSaved: () => Promise.all([loadOverview(), onSaved()]),
    });
  });
  section.append(form);
  return section;
}

function belegActionField(beleg) {
  const field = detailField("Aktionen", "", true);
  const value = field.querySelector(".detail-value");
  value.classList.remove("is-empty");
  value.replaceChildren();
  const actions = mailElement("div", "document-actions");
  actions.append(
    originalDocumentLink(beleg.beleg_id, Boolean(beleg.vorhanden)),
  );
  value.append(actions);
  return field;
}

function originalDocumentLink(belegId, enabled = true) {
  const link = document.createElement("a");
  link.className = "secondary-action document-open-action";
  link.href = `/api/belege/${encodeURIComponent(belegId)}/document`;
  link.target = "_blank";
  link.rel = "noopener";
  link.textContent = "Originaldokument öffnen";
  if (!enabled) {
    link.removeAttribute("href");
    link.removeAttribute("target");
    link.setAttribute("aria-disabled", "true");
    link.title = "Originaldatei ist nicht vorhanden";
  }
  return link;
}

function entityVorgangSelect(vorgaenge, selectedIds = [], single = false) {
  const container = mailElement("div", "is-wide assignment-picker");
  const label = mailElement("label", "assignment-search");
  label.append(mailElement("span", "detail-label", "Vorgänge suchen und auswählen"));
  const search = document.createElement("input");
  search.type = "search";
  search.placeholder = "Titel, Typ oder Status durchsuchen";
  label.append(search);
  const select = document.createElement("select");
  select.name = "vorgangs_ids";
  select.multiple = !single;
  select.size = 7;
  const selected = new Set(selectedIds || []);
  for (const vorgang of vorgaenge) {
    const option = document.createElement("option");
    option.value = vorgang.vorgangs_id;
    option.textContent = vorgangOptionLabel(vorgang);
    option.dataset.searchText = option.textContent.toLocaleLowerCase("de-DE");
    option.selected = selected.has(vorgang.vorgangs_id);
    select.append(option);
  }
  const empty = mailElement("p", "assignment-empty-hint");
  if (!vorgaenge.length) empty.textContent = "Keine Vorgänge verfügbar.";
  search.addEventListener("input", () => {
    const query = search.value.trim().toLocaleLowerCase("de-DE");
    let visible = 0;
    for (const option of select.options) {
      option.hidden = Boolean(query) && !option.dataset.searchText.includes(query);
      if (!option.hidden) visible += 1;
    }
    empty.textContent = visible ? "" : "Keine Vorgänge zur Suche gefunden.";
  });
  container.append(label, select, empty);
  return container;
}

function entityFormActions(label) {
  const container = mailElement("div", "vorgang-form-actions");
  const submit = mailElement("button", "primary-action", label);
  submit.type = "submit";
  const status = mailElement("span", "save-state");
  container.append(submit, status);
  return {container, submit, status};
}

function readVorgangForm(form) {
  const payload = {
    title: form.elements.title.value,
    description: form.elements.description.value,
    vorgangstyp: form.elements.vorgangstyp.value,
    completed: form.elements.completed.checked,
  };
  return {...payload, ...readSuggestionFields(form)};
}

function readSuggestionFields(form) {
  const payload = {};
  for (const section of form.querySelectorAll("[data-suggestion-field]")) {
    payload[section.dataset.suggestionField] = [
      ...section.querySelectorAll("input[type='checkbox']:checked"),
    ].map((checkbox) => checkbox.value);
  }
  return payload;
}

async function openVorgang(vorgangsId) {
  elements.dialog.classList.add("is-vorgang");
  elements.dialog.classList.remove("has-rule-workspace");
  elements.dialog.dataset.vorgangId = vorgangsId;
  elements.detailEyebrow.textContent = "Vorgangsdetails";
  elements.detailTitle.textContent = "Vorgang wird geladen";
  elements.detailSubtitle.textContent = "";
  elements.detailContent.replaceChildren(createLoadingBlock());
  elements.dialog.showModal();
  try {
    await loadVorgangWorkspace(vorgangsId);
  } catch (error) {
    elements.dialog.close();
    showError(error.message);
  }
}

async function loadVorgangWorkspace(vorgangsId, ruleStatus = "") {
  const [
    vorgangResponse,
    rulesResponse,
    completionRulesResponse,
    optionsResponse,
    assignmentResponse,
    suggestionsPayload,
  ] = await Promise.all([
    fetch(`/api/vorgaenge/${encodeURIComponent(vorgangsId)}`),
    fetch("/api/rules"),
    fetch("/api/completion-rules"),
    fetch("/api/classification-options"),
    fetch(`/api/vorgaenge/${encodeURIComponent(vorgangsId)}/mail-dokumentzuordnungen`),
    loadVorgangTypes(),
    loadVorgangSuggestions("vorgang", vorgangsId).catch(() => null),
  ]);
  const [
    vorgangPayload,
    rulesPayload,
    completionRulesPayload,
    options,
    assignmentPayload,
  ] = await Promise.all([
    readResponse(vorgangResponse),
    readResponse(rulesResponse),
    readResponse(completionRulesResponse),
    readResponse(optionsResponse),
    readResponse(assignmentResponse),
  ]);
  state.ruleMatchFields = rulesPayload.match_fields;
  state.ruleMatchOperators = rulesPayload.match_operators;
  state.ruleLogicConnectors = rulesPayload.logic_connectors;
  state.completionRuleMatchFields = completionRulesPayload.match_fields;
  state.classificationOptions = options;
  renderVorgangWorkspace(
    vorgangPayload.vorgang,
    rulesPayload,
    completionRulesPayload,
    ruleStatus,
    suggestionsPayload,
    assignmentPayload,
  );
}

async function openTransaction(transaktionsId) {
  elements.dialog.classList.remove("is-vorgang");
  elements.dialog.classList.add("has-rule-workspace");
  delete elements.dialog.dataset.vorgangId;
  delete elements.dialog.dataset.vorgangTransactionCount;
  elements.detailEyebrow.textContent = "Transaktionsdetails";
  elements.detailTitle.textContent = "Transaktion wird geladen";
  elements.detailSubtitle.textContent = "";
  elements.detailDialogStatus.textContent = "";
  elements.detailContent.replaceChildren(createLoadingBlock());
  elements.dialog.showModal();
  try {
    await loadTransactionWorkspace(transaktionsId);
  } catch (error) {
    elements.dialog.close();
    showError(error.message);
  }
}

async function loadTransactionWorkspace(transaktionsId, ruleStatus = "") {
  const [
    transactionResponse,
    splitsResponse,
    rulesResponse,
    completionRulesResponse,
    optionsResponse,
    suggestionsPayload,
  ] = await Promise.all([
    fetch(`/api/transactions/${encodeURIComponent(transaktionsId)}`),
    fetch(`/api/transactions/${encodeURIComponent(transaktionsId)}/splits`),
    fetch("/api/rules"),
    fetch("/api/completion-rules"),
    fetch("/api/classification-options"),
    loadVorgangSuggestions("transaction", transaktionsId).catch(() => null),
  ]);
  const [payload, splitsPayload, rulesPayload, completionRulesPayload, options] = await Promise.all([
    readResponse(transactionResponse),
    readResponse(splitsResponse),
    readResponse(rulesResponse),
    readResponse(completionRulesResponse),
    readResponse(optionsResponse),
  ]);
  state.ruleMatchFields = rulesPayload.match_fields;
  state.completionRuleMatchFields = completionRulesPayload.match_fields;
  state.ruleMatchOperators = completionRulesPayload.match_operators;
  state.ruleLogicConnectors = completionRulesPayload.logic_connectors;
  state.classificationOptions = options;
  payload.transaction.splits = splitsPayload.splits || [];
  payload.transaction.zulaessige_vorgaenge =
    splitsPayload.zulaessige_vorgaenge || [];
  renderDetail(
    payload.transaction,
    rulesPayload,
    completionRulesPayload,
    ruleStatus,
    suggestionsPayload,
  );
}

function renderDetail(
  transaction,
  rulesPayload,
  completionRulesPayload,
  ruleStatus = "",
  suggestionsPayload = null,
) {
  elements.detailTitle.textContent =
    transaction.zahlungsbeteiligter || transaction.kontoname;
  elements.detailSubtitle.textContent =
    `${formatDate(transaction.datum)} · ${transaction.kontoname}`;
  elements.detailDialogStatus.textContent = "";
  elements.detailContent.replaceChildren();
  const layout = document.createElement("div");
  layout.className = "vorgang-workspace";
  const details = document.createElement("div");
  details.className = "vorgang-workspace-details";
  layout.append(
    details,
    createClassificationRuleManager(
      rulesPayload,
      completionRulesPayload,
      async (message) => {
        state.rulesLoaded = false;
        state.vorgaengeLoaded = false;
        loadTransactions();
        if (!elements.vorgaengePanel.hidden) {
          loadVorgaenge();
        }
        await loadTransactionWorkspace(
          transaction.transaktions_id,
          message,
        );
      },
      ruleStatus,
    ),
  );
  elements.detailContent.append(layout);
  renderTransactionContent(transaction, details, suggestionsPayload);
}

function renderVorgangWorkspace(
  vorgang,
  rulesPayload,
  completionRulesPayload,
  ruleStatus = "",
  suggestionsPayload = null,
  assignmentPayload = null,
) {
  elements.dialog.dataset.vorgangId = vorgang.vorgangs_id;
  elements.dialog.dataset.vorgangTransactionCount =
    String(vorgang.transaktionen.length);
  elements.detailEyebrow.textContent = "Vorgangsdetails";
  elements.detailTitle.textContent =
    vorgang.titel || vorgang.vorgangstyp || "Vorgang ohne Titel";
  elements.detailSubtitle.textContent =
    `${formatStatus(vorgang.status)} \u00b7 ` +
    entityCountSummary(vorgang);
  elements.detailDialogStatus.textContent = "";
  elements.detailContent.replaceChildren();

  const layout = document.createElement("div");
  layout.className = "vorgang-workspace";
  const details = document.createElement("div");
  details.className = "vorgang-workspace-details";
  layout.append(
    details,
    createVorgangRuleManager(
      vorgang,
      rulesPayload,
      completionRulesPayload,
      ruleStatus,
    ),
  );
  elements.detailContent.append(layout);

  details.append(createVorgangStatusEditor(vorgang));
  details.append(createVorgangMetadataEditor(vorgang, suggestionsPayload));
  details.append(createDonationCertificateAction(vorgang));
  details.append(createMailDocumentAssignmentEditor(vorgang, assignmentPayload));
  appendDetailSection("Vorgang", [
    detailField("Vorgangs-ID", vorgang.vorgangs_id, true, true),
    detailField("Titel", vorgang.titel, true),
    detailField("Beschreibung", vorgang.beschreibung, true),
    detailField(
      "Vorgangstyp",
      vorgang.vorgangstyp,
      false,
      false,
      vorgang.vorgangs_id,
      "vorgangstyp",
    ),
    detailField(
      "Status",
      formatStatus(vorgang.status),
      false,
      false,
      vorgang.vorgangs_id,
      "status",
    ),
    detailField("Erstellt", formatDateTime(vorgang.erstellt_am)),
    detailField(
      "Aktualisiert",
      formatDateTime(vorgang.aktualisiert_am),
      false,
      false,
      vorgang.vorgangs_id,
      "aktualisiert_am",
    ),
  ], details);

  appendVorgangEntitySections(vorgang, details);
  for (const transaction of vorgang.transaktionen) {
    const heading = document.createElement("div");
    heading.className = "entity-heading";
    heading.textContent =
      transaction.zahlungsbeteiligter ||
      `Transaktion ${transaction.transaktions_id}`;
    details.append(heading);
    renderTransactionContent(transaction, details);
  }
}

function createDonationCertificateAction(vorgang) {
  const section = mailElement("section", "detail-section");
  section.append(mailElement("h3", "", "Spendenbescheinigung"));
  const form = mailElement("form", "vorgang-edit-form");
  const recipient = formTextField("Empfänger-ID", "recipient_id", "", true);
  const actions = mailElement("div", "vorgang-form-actions");
  const button = mailElement("button", "primary-action", "Entwurf erzeugen");
  button.type = "submit";
  actions.append(button);
  form.append(recipient, actions);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    button.disabled = true;
    try {
      await requestJson(
        `/api/vorgaenge/${encodeURIComponent(vorgang.vorgangs_id)}/spendenbescheinigung`,
        {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify({recipient_id: form.elements.recipient_id.value})},
      );
      await loadVorgangWorkspace(vorgang.vorgangs_id, "Spendenbescheinigung erzeugt");
    } catch (error) {
      elements.detailDialogStatus.textContent = error.message;
    } finally {
      button.disabled = false;
    }
  });
  section.append(form);
  return section;
}

function createMailDocumentAssignmentEditor(vorgang, payload) {
  const section = mailElement(
    "section",
    "detail-section mail-document-assignment-editor",
  );
  section.append(mailElement("h3", "", "Dokumente Transaktionen zuordnen"));
  const documents = payload?.dokumente || [];
  const transactions = payload?.transaktionen || [];
  if (!documents.length) {
    section.append(mailElement("p", "empty-state", "Diesem Vorgang sind keine Dokumente zugeordnet."));
    return section;
  }

  const assignments = new Map(
    (payload?.zuordnungen || []).map((item) => [
      item.beleg_id,
      item.transaktions_id || "",
    ]),
  );
  const form = mailElement("form", "mail-document-assignment-form");
  const list = mailElement("div", "mail-document-assignment-list");
  for (const documentItem of documents) {
    const row = mailElement("label", "mail-document-assignment-row");
    const description = mailElement("span", "mail-document-assignment-document");
    description.append(
      mailElement("strong", "", documentItem.dateiname || documentItem.beleg_id),
    );
    const metadata = [
      documentItem.kategorie,
      documentItem.dokumentdatum ? formatDate(documentItem.dokumentdatum) : "",
      documentItem.betrag ? currencyFormatter.format(Number(documentItem.betrag)) : "",
      documentItem.mail_inbox_id
        ? `Mail-Anhang${documentItem.mail_attachment_index !== null ? ` ${Number(documentItem.mail_attachment_index) + 1}` : ""}`
        : "",
    ].filter(Boolean).join(" · ");
    if (metadata) {
      description.append(mailElement("span", "mail-document-assignment-meta", metadata));
    }
    const select = document.createElement("select");
    select.name = "document_assignment";
    select.dataset.belegId = documentItem.beleg_id;
    select.append(new Option("Keine spezifische Transaktion", ""));
    for (const transaction of transactions) {
      select.append(new Option(mailDocumentTransactionLabel(transaction), transaction.transaktions_id));
    }
    select.value = assignments.get(documentItem.beleg_id) || "";
    select.dataset.confirmedValue = select.value;
    row.append(description, select);
    list.append(row);
  }
  form.append(list);
  if (!transactions.length) {
    form.append(mailElement("p", "assignment-empty-hint", "Dieser Vorgang hat keine verknüpften Transaktionen. Dokumente können nur ohne spezifische Transaktion gespeichert werden."));
  }
  const actions = mailElement("div", "vorgang-form-actions");
  const submit = mailElement("button", "primary-action", "Zuordnungen speichern");
  submit.type = "submit";
  const status = mailElement("span", "save-state");
  actions.append(submit, status);
  form.append(actions);
  const assignmentSelects = () => [
    ...form.querySelectorAll("select[data-beleg-id]"),
  ];
  const updateChangedState = () => {
    const changed = assignmentSelects().some(
      (select) => select.value !== select.dataset.confirmedValue,
    );
    submit.disabled = !changed;
    if (!changed && !status.classList.contains("is-saved")) {
      status.textContent = "Keine Änderungen";
    }
  };
  form.addEventListener("change", updateChangedState);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    submit.disabled = true;
    status.className = "save-state is-saving";
    status.textContent = "Wird gespeichert";
    const zuordnungen = assignmentSelects().map((select) => ({
      beleg_id: select.dataset.belegId,
      transaktions_id: select.value || null,
    }));
    try {
      const response = await fetch(
        `/api/vorgaenge/${encodeURIComponent(vorgang.vorgangs_id)}/mail-dokumentzuordnungen`,
        {
          method: "PUT",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({zuordnungen}),
        },
      );
      await readResponse(response);
      await loadVorgangWorkspace(vorgang.vorgangs_id, "Dokumentzuordnungen gespeichert");
    } catch (error) {
      status.className = "save-state is-error";
      status.textContent = `Speichern fehlgeschlagen: ${error.message}`;
      submit.disabled = false;
      showError(error.message);
    }
  });
  updateChangedState();
  section.append(form);
  return section;
}

function mailDocumentTransactionLabel(transaction) {
  const description = transaction.zahlungsbeteiligter || transaction.verwendungszweck || transaction.transaktions_id;
  const amount = transaction.betrag === null || transaction.betrag === undefined || transaction.betrag === ""
    ? ""
    : currencyFormatter.format(Number(transaction.betrag));
  return [formatDate(transaction.datum), description, amount].filter(Boolean).join(" · ");
}

function entityCountSummary(vorgang) {
  const parts = [
    countLabel(vorgang.transaktionen?.length || 0, "Transaktion", "Transaktionen"),
    countLabel(vorgang.mails?.length || 0, "Mail", "Mails"),
    countLabel(vorgang.todos?.length || 0, "To-Do", "To-Dos"),
    countLabel(vorgang.belege?.length || 0, "Dokument", "Dokumente"),
    countLabel(vorgang.termine?.length || 0, "Termin", "Termine"),
  ].filter(Boolean);
  return parts.join(" · ") || "Keine Entitäten";
}

function countLabel(count, singular, plural) {
  return count ? `${count} ${count === 1 ? singular : plural}` : "";
}

function createVorgangMetadataEditor(vorgang, suggestionsPayload = null) {
  const section = mailElement("section", "detail-section vorgang-edit-section");
  section.append(mailElement("h3", "", "Vorgang bearbeiten"));
  const form = mailElement("form", "vorgang-edit-form");
  form.append(
    formTextField("Titel", "title", vorgang.titel || "", false),
    formVorgangTypeField("vorgangstyp", vorgang.vorgangstyp || ""),
    formTextField(
      "Beschreibung",
      "description",
      vorgang.beschreibung || "",
      false,
      true,
    ),
  );
  form.append(
    createSuggestionSection(
      "Transaktionen",
      "transaction_ids",
      (vorgang.transaktionen || []).map((item) => item.transaktions_id),
      linkItems(suggestionsPayload, "transactions"),
    ),
    createSuggestionSection(
      "Mails",
      "mail_ids",
      (vorgang.mails || []).map((item) => item.inbox_id),
      linkItems(suggestionsPayload, "mails"),
    ),
    createSuggestionSection(
      "To-Dos",
      "todo_ids",
      (vorgang.todos || []).map((item) => item.todo_id),
      linkItems(suggestionsPayload, "todos"),
      "todo",
    ),
    createSuggestionSection(
      "Dokumente",
      "beleg_ids",
      (vorgang.belege || []).map((item) => item.beleg_id),
      linkItems(suggestionsPayload, "belege"),
    ),
    createSuggestionSection(
      "Termine",
      "termin_ids",
      (vorgang.termine || []).map((item) => item.termin_id),
      linkItems(suggestionsPayload, "termine"),
      "termin",
    ),
  );
  const actions = mailElement("div", "vorgang-form-actions");
  const submit = mailElement("button", "primary-action", "Änderungen speichern");
  submit.type = "submit";
  const status = mailElement("span", "save-state");
  actions.append(submit, status);
  form.append(actions);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    submit.disabled = true;
    status.className = "save-state is-saving";
    status.textContent = "Wird gespeichert";
    try {
      const response = await fetch(
        `/api/vorgaenge/${encodeURIComponent(vorgang.vorgangs_id)}`,
        {
          method: "PATCH",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify(readVorgangEditForm(form, vorgang)),
        },
      );
      await readResponse(response);
      rememberVorgangType(form.elements.vorgangstyp.value);
      state.vorgaengeLoaded = false;
      state.todosLoaded = false;
      state.termineLoaded = false;
      await Promise.all([loadOverview(), loadVorgaenge()]);
      await loadVorgangWorkspace(vorgang.vorgangs_id, "Vorgang gespeichert");
    } catch (error) {
      submit.disabled = false;
      status.className = "save-state is-error";
      status.textContent = "Speichern fehlgeschlagen";
      showError(error.message);
    }
  });
  section.append(form);
  return section;
}

function formIdListField(labelText, name, ids) {
  const label = mailElement("label", "is-wide");
  label.append(mailElement("span", "detail-label", labelText));
  const textarea = document.createElement("textarea");
  textarea.name = name;
  textarea.rows = 2;
  textarea.value = (ids || []).join("\n");
  label.append(textarea);
  return label;
}

function readVorgangEditForm(form, vorgang) {
  const links = readSuggestionFields(form);
  return {
    title: form.elements.title.value,
    description: form.elements.description.value,
    vorgangstyp: form.elements.vorgangstyp.value,
    completed: vorgang.status === "abgeschlossen",
    transaction_ids: links.transaction_ids || [],
    mail_ids: links.mail_ids || [],
    todo_ids: links.todo_ids || [],
    beleg_ids: links.beleg_ids || [],
    termin_ids: links.termin_ids || [],
  };
}

function splitIdList(value) {
  return String(value || "")
    .split(/[\n,;]+/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function appendVorgangEntitySections(vorgang, details) {
  const entityFields = [];
  for (const mail of vorgang.mails || []) {
    entityFields.push(
      detailField(
        mail.subject || mail.inbox_id,
        [mail.sender_name, mail.received_at].filter(Boolean).join(" · "),
        true,
      ),
    );
  }
  for (const todo of vorgang.todos || []) {
    entityFields.push(
      detailField(
        todo.title || todo.todo_id,
        [todo.priority, todo.due_date ? formatDate(todo.due_date) : ""]
          .filter(Boolean)
          .join(" · "),
        true,
      ),
    );
  }
  for (const termin of vorgang.termine || []) {
    entityFields.push(
      detailField(
        termin.title || termin.termin_id,
        [formatDateTime(termin.starts_at), termin.location]
          .filter(Boolean)
          .join(" · "),
        true,
      ),
    );
  }
  for (const beleg of vorgang.belege || []) {
    const field = detailField(
      beleg.dateiname || beleg.beleg_id,
      beleg.vorhanden
        ? beleg.dateipfad
        : `${beleg.dateipfad} (Datei nicht vorhanden)`,
      true,
      true,
    );
    const value = field.querySelector(".detail-value");
    const actions = mailElement("div", "document-actions");
    const catalogButton = mailElement(
      "button",
      "suggestion-open-action",
      "Katalogeintrag öffnen",
    );
    catalogButton.type = "button";
    catalogButton.addEventListener("click", () => {
      openEntityPreview("beleg", beleg.beleg_id);
    });
    actions.append(
      catalogButton,
      originalDocumentLink(beleg.beleg_id, Boolean(beleg.vorhanden)),
    );
    value.append(actions);
    entityFields.push(field);
  }
  appendDetailSection(
    "Zugeordnete Entitäten",
    entityFields.length ? entityFields : [detailField("Entitäten", "")],
    details,
  );
}

function createVorgangStatusEditor(vorgang) {
  const section = document.createElement("section");
  section.className = "detail-section vorgang-status-editor";
  const headingRow = document.createElement("div");
  headingRow.className = "vorgang-status-heading";
  const heading = document.createElement("h3");
  heading.textContent = "Bearbeitungsstatus";
  const saveState = document.createElement("span");
  saveState.className = "save-state";
  saveState.textContent = vorgang.status_manuell
    ? "Manuell gesetzt"
    : "Automatisch ermittelt";
  headingRow.append(heading, saveState);

  const currentStatus = mailElement("div", "vorgang-status-current");
  currentStatus.append(
    mailElement("span", "detail-label", "Aktueller Status"),
    statusBadge(vorgang.status),
  );

  const isCompleted = vorgang.status === "abgeschlossen";
  const canComplete = Boolean(vorgang.abschluss_moeglich);
  const blockers = vorgang.abschluss_blocker || [];
  const completionChecks = vorgang.abschluss_pruefung || [];
  const description = document.createElement("p");
  description.className = "vorgang-status-description";
  description.textContent = isCompleted
    ? "Der Vorgang ist abgeschlossen und kann bei Bedarf wieder geöffnet werden."
    : canComplete
      ? "Alle Abschlussbedingungen sind erfüllt."
      : (
        (completionChecks.length
          ? "Folgende Abschlussbedingungen sind noch offen."
          : blockers.join(" ")) ||
        "Vor dem Abschluss müssen bei allen Transaktionen Transaktionstyp, " +
        "Oberkategorie, Unterkategorie und Sphäre ausgefüllt sein."
      );

  const actions = mailElement("div", "vorgang-status-actions");
  const statusButton = mailElement(
    "button",
    isCompleted || canComplete ? "primary-action" : "secondary-action",
    isCompleted ? "Vorgang wieder öffnen" : "Vorgang abschließen",
  );
  statusButton.type = "button";
  statusButton.disabled = !isCompleted && !canComplete;
  actions.append(statusButton);

  if (!isCompleted && completionChecks.length) {
    const checklist = document.createElement("ul");
    checklist.className = "vorgang-completion-checklist";
    for (const check of completionChecks) {
      const item = document.createElement("li");
      item.className = `is-${check.status || "offen"}`;
      const stateLabel = check.status === "erfuellt" ? "Erfüllt" : "Offen";
      item.append(
        mailElement("span", "completion-check-state", stateLabel),
        mailElement("strong", "", check.title || "Abschlussbedingung"),
        mailElement("span", "completion-check-message", check.message || ""),
      );
      if (check.action) {
        item.append(mailElement("span", "completion-check-action", check.action));
      }
      checklist.append(item);
    }
    actions.append(checklist);
  } else if (!isCompleted && !canComplete && blockers.length) {
    const blockerList = document.createElement("ul");
    blockerList.className = "vorgang-status-blockers";
    for (const blocker of blockers) {
      blockerList.append(mailElement("li", "", blocker));
    }
    actions.append(blockerList);
  }

  statusButton.addEventListener("click", async () => {
    const completed = !isCompleted;
    statusButton.disabled = true;
    saveState.className = "save-state is-saving";
    saveState.textContent = "Wird gespeichert";
    try {
      const response = await fetch(
        `/api/vorgaenge/${encodeURIComponent(vorgang.vorgangs_id)}/status`,
        {
          method: "PATCH",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ completed }),
        },
      );
      const payload = await readResponse(response);
      Object.assign(vorgang, payload.vorgang);
      updateVorgangDisplays([vorgang]);
      saveState.className = "save-state is-saved";
      saveState.textContent = "Gespeichert";
      state.vorgaengeLoaded = false;
      state.todosLoaded = false;
      state.termineLoaded = false;
      const refreshes = [loadOverview(), loadTransactions()];
      if (!elements.vorgaengePanel.hidden) {
        refreshes.push(loadVorgaenge());
      }
      await Promise.all(refreshes);
      await loadVorgangWorkspace(
        vorgang.vorgangs_id,
        completed ? "Vorgang abgeschlossen" : "Vorgang wieder geöffnet",
      );
    } catch (error) {
      statusButton.disabled = !isCompleted && !canComplete;
      saveState.className = "save-state is-error";
      saveState.textContent = "Speichern fehlgeschlagen";
      showError(error.message);
    }
  });

  const deleteActions = mailElement("div", "vorgang-form-actions");
  const deleteButton = mailElement(
    "button",
    "secondary-action danger-action",
    "Vorgang löschen",
  );
  deleteButton.type = "button";
  deleteButton.addEventListener("click", () => deleteVorgang(vorgang, deleteButton));
  deleteActions.append(deleteButton);

  section.append(headingRow, currentStatus, description, actions, deleteActions);
  return section;
}

async function deleteVorgang(vorgang, button) {
  if (!window.confirm("Diesen Vorgang wirklich löschen?")) {
    return;
  }
  button.disabled = true;
  try {
    const response = await fetch(
      `/api/vorgaenge/${encodeURIComponent(vorgang.vorgangs_id)}`,
      {method: "DELETE"},
    );
    await readResponse(response);
    state.vorgaengeLoaded = false;
    await Promise.all([loadOverview(), loadVorgaenge()]);
    if (elements.dialog.open) {
      elements.dialog.close();
    }
  } catch (error) {
    button.disabled = false;
    showError(error.message);
  }
}

function createClassificationRuleManager(
  rulesPayload,
  completionRulesPayload,
  refreshWorkspace,
  ruleStatus = "",
) {
  const manager = document.createElement("aside");
  manager.className = "vorgang-rule-manager";
  const heading = document.createElement("h3");
  heading.textContent = "Regeln";
  const description = document.createElement("p");
  description.className = "vorgang-rule-description";
  description.textContent =
    "Regeln erstellen oder bearbeiten, w\u00e4hrend der Vorgang sichtbar bleibt.";

  const listHeading = document.createElement("div");
  listHeading.className = "subsection-heading";
  const listTitle = document.createElement("h4");
  listTitle.textContent = "Aktuelle Regeln";
  const count = document.createElement("span");
  listHeading.append(listTitle, count);

  const searchLabel = document.createElement("label");
  searchLabel.className = "rule-search";
  const searchText = document.createElement("span");
  searchText.textContent = "Regeln durchsuchen";
  const search = document.createElement("input");
  search.type = "search";
  search.autocomplete = "off";
  search.placeholder = "Name, Bedingung oder Klassifikation";
  searchLabel.append(searchText, search);

  const list = document.createElement("div");
  list.className = "rule-list vorgang-rule-list";
  const listPanel = document.createElement("div");
  listPanel.className = "vorgang-rule-list-panel";
  listPanel.hidden = true;
  listPanel.append(listHeading, searchLabel, list);
  const listToggle = document.createElement("button");
  listToggle.className = "vorgang-rule-list-toggle";
  listToggle.type = "button";
  listToggle.setAttribute("aria-expanded", "false");
  const updateListToggle = () => {
    listToggle.textContent = listPanel.hidden
      ? `Aktuelle Regeln anzeigen (${rulesPayload.rules.length})`
      : "Aktuelle Regeln ausblenden";
    listToggle.setAttribute(
      "aria-expanded",
      String(!listPanel.hidden),
    );
  };
  listToggle.addEventListener("click", () => {
    listPanel.hidden = !listPanel.hidden;
    updateListToggle();
  });

  const form = elements.ruleForm.cloneNode(true);
  form.classList.add("vorgang-rule-form");
  const formTitle = form.querySelector("#rule-form-title");
  const submit = form.querySelector("#rule-submit");
  const cancel = form.querySelector("#rule-cancel-edit");
  const formStatus = form.querySelector("#rule-form-status");
  const conditionContainer = form.querySelector("#rule-conditions");
  const addCondition = form.querySelector("#rule-add-condition");
  conditionContainer.classList.add("rule-condition-list");
  formStatus.classList.add("rule-form-status");
  form.removeAttribute("id");
  form.querySelectorAll("[id]").forEach((element) => {
    element.removeAttribute("id");
  });

  let editingRuleId = null;
  const rules = rulesPayload.rules;

  const resetForm = () => {
    editingRuleId = null;
    for (const field of [
      "name",
      "transaction_type",
      "top_category",
      "sub_category",
      "sphere",
      "professional_description",
    ]) {
      form.elements[field].value = "";
    }
    form.elements.enabled.checked = true;
    form.elements.apply_now.checked = true;
    conditionContainer.replaceChildren();
    addRuleCondition({}, conditionContainer, addCondition);
    configureRuleClassificationFields(form);
    formTitle.textContent = "Neue Regel";
    submit.textContent = "Regel erstellen";
    cancel.hidden = true;
    formStatus.textContent = "";
  };

  const edit = (rule) => {
    editingRuleId = rule.rule_id;
    formTitle.textContent = `Regel bearbeiten: ${rule.name}`;
    submit.textContent = "\u00c4nderungen speichern";
    cancel.hidden = false;
    for (const field of [
      "name",
      "transaction_type",
      "top_category",
      "sub_category",
      "sphere",
      "professional_description",
    ]) {
      form.elements[field].value = rule[field] || "";
    }
    form.elements.enabled.checked = rule.enabled;
    form.elements.apply_now.checked = false;
    const conditions = rule.conditions?.length
      ? rule.conditions
      : [{
        connector: "",
        match_field: rule.match_field,
        match_operator: rule.match_operator,
        match_value: rule.match_value,
      }];
    conditionContainer.replaceChildren();
    conditions.forEach((condition) => {
      addRuleCondition(condition, conditionContainer, addCondition);
    });
    configureRuleClassificationFields(form);
    formStatus.textContent =
      "Felder bearbeiten und anschlie\u00dfend speichern";
    form.scrollIntoView({behavior: "smooth", block: "nearest"});
  };

  const remove = async (rule) => {
    if (!window.confirm(`Regel "${rule.name}" wirklich entfernen?`)) {
      return;
    }
    formStatus.textContent = "Regel wird entfernt";
    try {
      const response = await fetch(
        `/api/rules/${encodeURIComponent(rule.rule_id)}`,
        {method: "DELETE"},
      );
      await readResponse(response);
      await refreshWorkspace("Regel entfernt");
    } catch (error) {
      formStatus.textContent = "Entfernen fehlgeschlagen";
      showError(error.message);
    }
  };

  const renderList = () => {
    const query = search.value.trim().toLocaleLowerCase("de-DE");
    const filtered = query
      ? rules.filter((rule) =>
        [
          rule.name,
          formatRuleConditions(rule),
          rule.transaction_type,
          rule.top_category,
          rule.sub_category,
          rule.sphere,
          rule.professional_description,
        ].join(" ").toLocaleLowerCase("de-DE").includes(query)
      )
      : rules;
    count.textContent =
      `${integerFormatter.format(filtered.length)} ` +
      `${filtered.length === 1 ? "Regel" : "Regeln"}`;
    renderRuleCards(list, filtered, edit, remove);
  };

  search.addEventListener("input", renderList);
  addCondition.addEventListener("click", () => {
    addRuleCondition({}, conditionContainer, addCondition);
  });
  cancel.addEventListener("click", resetForm);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    submit.disabled = true;
    const editing = Boolean(editingRuleId);
    formStatus.textContent = editing
      ? "Regel wird gespeichert"
      : "Regel wird erstellt";
    const payload = Object.fromEntries(new FormData(form).entries());
    payload.enabled = form.elements.enabled.checked;
    payload.apply_now = form.elements.apply_now.checked;
    try {
      payload.conditions = readRuleConditions(conditionContainer);
      const endpoint = editing
        ? `/api/rules/${encodeURIComponent(editingRuleId)}`
        : "/api/rules";
      const response = await fetch(endpoint, {
        method: editing ? "PATCH" : "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload),
      });
      const result = await readResponse(response);
      const message = result.applied
        ? `${result.changed_transactions} Transaktionen klassifiziert`
        : editing ? "Regel aktualisiert" : "Regel gespeichert";
      await refreshWorkspace(message);
    } catch (error) {
      submit.disabled = false;
      formStatus.textContent = editing
        ? "Speichern fehlgeschlagen"
        : "Erstellen fehlgeschlagen";
      showError(error.message);
    }
  });

  resetForm();
  formStatus.textContent = ruleStatus;
  renderList();
  updateListToggle();
  manager.append(
    heading,
    description,
    listToggle,
    listPanel,
    form,
    createCompletionRuleManager(
      completionRulesPayload,
      refreshWorkspace,
      "Abschlussregeln",
      ruleStatus,
    ),
  );
  return manager;
}

function createVorgangRuleManager(
  vorgang,
  rulesPayload,
  completionRulesPayload,
  ruleStatus = "",
) {
  const refreshWorkspace = async (message) => {
    state.rulesLoaded = false;
    state.vorgaengeLoaded = false;
    loadTransactions();
    if (!elements.vorgaengePanel.hidden) {
      loadVorgaenge();
    }
    await loadVorgangWorkspace(vorgang.vorgangs_id, message);
  };
  return createClassificationRuleManager(
    rulesPayload,
    completionRulesPayload,
    refreshWorkspace,
    ruleStatus,
  );
}

function createCompletionRuleManager(
  rulesPayload,
  refreshWorkspace,
  titleText = "Abschlussregeln",
  ruleStatus = "",
  standalone = false,
) {
  const manager = document.createElement("section");
  manager.className = standalone
    ? "vorgang-rule-manager embedded-completion-rules is-standalone"
    : "embedded-completion-rules";
  const heading = document.createElement("h3");
  heading.textContent = titleText;
  const description = document.createElement("p");
  description.className = "vorgang-rule-description";
  description.textContent =
    "Diese Regeln werden nach der Klassifikation geprüft und schließen " +
    "passende Vorgänge automatisch ab.";

  const list = document.createElement("div");
  list.className = "rule-list vorgang-rule-list";
  const listPanel = document.createElement("div");
  listPanel.className = "vorgang-rule-list-panel";
  listPanel.hidden = true;
  const listHeading = document.createElement("div");
  listHeading.className = "subsection-heading";
  const listTitle = document.createElement("h4");
  listTitle.textContent = "Aktuelle Abschlussregeln";
  const count = document.createElement("span");
  listHeading.append(listTitle, count);
  const searchLabel = document.createElement("label");
  searchLabel.className = "rule-search";
  const searchText = document.createElement("span");
  searchText.textContent = "Abschlussregeln durchsuchen";
  const search = document.createElement("input");
  search.type = "search";
  search.autocomplete = "off";
  search.placeholder = "Name, Bedingung oder Klassifikation";
  searchLabel.append(searchText, search);
  listPanel.append(listHeading, searchLabel, list);

  const listToggle = document.createElement("button");
  listToggle.className = "vorgang-rule-list-toggle";
  listToggle.type = "button";
  listToggle.setAttribute("aria-expanded", "false");
  const updateListToggle = () => {
    listToggle.textContent = listPanel.hidden
      ? `Abschlussregeln anzeigen (${rulesPayload.rules.length})`
      : "Abschlussregeln ausblenden";
    listToggle.setAttribute(
      "aria-expanded",
      String(!listPanel.hidden),
    );
  };
  listToggle.addEventListener("click", () => {
    listPanel.hidden = !listPanel.hidden;
    updateListToggle();
  });

  const form = elements.completionRuleForm.cloneNode(true);
  form.classList.add("vorgang-rule-form");
  const formTitle = form.querySelector("#completion-rule-form-title");
  const submit = form.querySelector("#completion-rule-submit");
  const cancel = form.querySelector("#completion-rule-cancel-edit");
  const formStatus = form.querySelector("#completion-rule-form-status");
  const conditionContainer = form.querySelector(
    "#completion-rule-conditions",
  );
  const addCondition = form.querySelector(
    "#completion-rule-add-condition",
  );
  conditionContainer.classList.add("rule-condition-list");
  formStatus.classList.add("rule-form-status");
  form.removeAttribute("id");
  form.querySelectorAll("[id]").forEach((element) => {
    element.removeAttribute("id");
  });

  let editingRuleId = null;
  const rules = rulesPayload.rules;
  const matchFields = rulesPayload.match_fields;

  const resetForm = () => {
    editingRuleId = null;
    form.reset();
    form.elements.name.value = "";
    form.elements.enabled.checked = true;
    form.elements.apply_now.checked = true;
    conditionContainer.replaceChildren();
    addRuleCondition(
      {},
      conditionContainer,
      addCondition,
      matchFields,
    );
    formTitle.textContent = "Neue Abschlussregel";
    submit.textContent = "Abschlussregel erstellen";
    cancel.hidden = true;
    formStatus.textContent = "";
  };

  const edit = (rule) => {
    editingRuleId = rule.rule_id;
    formTitle.textContent = `Abschlussregel bearbeiten: ${rule.name}`;
    submit.textContent = "Änderungen speichern";
    cancel.hidden = false;
    form.elements.name.value = rule.name;
    form.elements.enabled.checked = rule.enabled;
    form.elements.apply_now.checked = true;
    const conditions = rule.conditions?.length
      ? rule.conditions
      : [{
        connector: "",
        match_field: rule.match_field,
        match_operator: rule.match_operator,
        match_value: rule.match_value,
      }];
    conditionContainer.replaceChildren();
    conditions.forEach((condition) => {
      addRuleCondition(
        condition,
        conditionContainer,
        addCondition,
        matchFields,
      );
    });
    formStatus.textContent =
      "Felder bearbeiten und anschließend speichern";
    form.scrollIntoView({behavior: "smooth", block: "nearest"});
  };

  const remove = async (rule) => {
    if (!window.confirm(
      `Abschlussregel "${rule.name}" wirklich entfernen?`,
    )) {
      return;
    }
    formStatus.textContent = "Abschlussregel wird entfernt";
    try {
      const response = await fetch(
        `/api/completion-rules/${encodeURIComponent(rule.rule_id)}`,
        {method: "DELETE"},
      );
      const result = await readResponse(response);
      await refreshWorkspace(
        `Abschlussregel entfernt, ${result.changed_vorgaenge} Vorgänge aktualisiert`,
      );
    } catch (error) {
      formStatus.textContent = "Entfernen fehlgeschlagen";
      showError(error.message);
    }
  };

  const renderList = () => {
    const query = search.value.trim().toLocaleLowerCase("de-DE");
    const filtered = query
      ? rules.filter((rule) =>
        [
          rule.name,
          formatRuleConditions(rule, matchFields),
        ].join(" ").toLocaleLowerCase("de-DE").includes(query)
      )
      : rules;
    count.textContent =
      `${integerFormatter.format(filtered.length)} ` +
      `${filtered.length === 1 ? "Regel" : "Regeln"}`;
    renderRuleCards(
      list,
      filtered,
      edit,
      remove,
      () => "Vorgang automatisch abschließen",
      matchFields,
    );
  };

  search.addEventListener("input", renderList);
  addCondition.addEventListener("click", () => {
    addRuleCondition(
      {},
      conditionContainer,
      addCondition,
      matchFields,
    );
  });
  cancel.addEventListener("click", resetForm);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    submit.disabled = true;
    const editing = Boolean(editingRuleId);
    formStatus.textContent = editing
      ? "Abschlussregel wird gespeichert"
      : "Abschlussregel wird erstellt";
    const payload = Object.fromEntries(new FormData(form).entries());
    payload.enabled = form.elements.enabled.checked;
    payload.apply_now = form.elements.apply_now.checked;
    try {
      payload.conditions = readRuleConditions(conditionContainer);
      const endpoint = editing
        ? `/api/completion-rules/${encodeURIComponent(editingRuleId)}`
        : "/api/completion-rules";
      const response = await fetch(endpoint, {
        method: editing ? "PATCH" : "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload),
      });
      const result = await readResponse(response);
      const message = result.applied
        ? `${result.changed_vorgaenge} Vorgänge aktualisiert`
        : editing
          ? "Abschlussregel aktualisiert"
          : "Abschlussregel gespeichert";
      await refreshWorkspace(message);
    } catch (error) {
      submit.disabled = false;
      formStatus.textContent = editing
        ? "Speichern fehlgeschlagen"
        : "Erstellen fehlgeschlagen";
      showError(error.message);
    }
  });

  resetForm();
  formStatus.textContent = ruleStatus;
  renderList();
  updateListToggle();
  manager.append(
    heading,
    description,
    listToggle,
    listPanel,
    form,
  );
  return manager;
}

function renderTransactionContent(
  transaction,
  target = elements.detailContent,
  suggestionsPayload = null,
) {

  const summary = document.createElement("div");
  summary.className = "detail-summary";
  const summaryText = document.createElement("div");
  const summaryLabel = document.createElement("span");
  summaryLabel.className = "detail-label";
  summaryLabel.textContent = "Verwendungszweck";
  const summaryPurpose = document.createElement("strong");
  summaryPurpose.textContent =
    transaction.verwendungszweck || "Ohne Verwendungszweck";
  summaryText.append(summaryLabel, summaryPurpose);
  const createButton = mailElement(
    "button",
    "secondary-action entity-create-vorgang",
    "Vorgang erstellen",
  );
  createButton.type = "button";
  createButton.addEventListener("click", () => {
    openVorgangCreateDialog({
      type: "transaction",
      id: transaction.transaktions_id,
      title: transaction.zahlungsbeteiligter || transaction.verwendungszweck,
      description: transaction.verwendungszweck || "",
    });
  });
  summary.append(summaryText, amountBadge(transaction.betrag), createButton);
  target.append(summary);

  appendDetailSection("Buchung", [
    detailField("Transaktions-ID", transaction.transaktions_id, true, true),
    detailField("Buchungsdatum", formatDate(transaction.datum)),
    detailField("Valutadatum", formatDate(transaction.valutadatum)),
    detailField("Kontoname", transaction.kontoname),
    detailField("Kontonummer", transaction.kontonummer, false, true),
    detailField("Zahlungsbeteiligter", transaction.zahlungsbeteiligter),
    detailField("Gegenkonto", transaction.gegenkonto, false, true),
    detailField("Buchungstext", transaction.buchungstext),
    detailField("Verwendungszweck", transaction.verwendungszweck, true),
    detailField("Währung", transaction.waehrung),
    detailField(
      "Kontostand Konto",
      formatOptionalCurrency(transaction.kontostand_konto),
    ),
    detailField(
      transaction.kontostand_gesamt_vollstaendig
        ? "Kontostand gesamt"
        : "Bekannter Gesamtstand",
      formatOptionalCurrency(transaction.kontostand_gesamt),
    ),
  ], target);

  appendClassificationEditor(transaction, target);
  appendSplitEditor(transaction, target);
  if (suggestionsPayload) {
    appendTransactionVorgangLinkSection(
      transaction,
      suggestionsPayload,
      target,
    );
  }

  appendDetailSection("Zuordnungen und Referenzen", [
    detailField(
      "Vorgangs-IDs",
      joinValues(transaction.vorgangs_ids),
      true,
      true,
    ),
    detailField("Gläubiger-ID", transaction.glaeubiger_id, false, true),
    detailField("Mandatsreferenz", transaction.mandatsreferenz, false, true),
    detailField("Quellinformation", transaction.quellinformation, true),
  ], target);

  appendSourceSection(transaction.quellen, target);

  appendDetailSection("Technische Informationen", [
    detailField("Provider", transaction.provider),
    detailField("Konto-ID", transaction.konto_id, false, true),
    detailField("Fingerprint", transaction.fingerprint, true, true),
    detailField("Vorkommen", transaction.vorkommen),
    detailField("Betrag in Cent", transaction.betrag_cent),
    detailField(
      "Zuerst importiert",
      formatDateTime(transaction.zuerst_importiert),
    ),
  ], target);

  appendRawDataSection(transaction.rohdaten, target);
}

function appendTransactionVorgangLinkSection(
  transaction,
  suggestionsPayload,
  target = elements.detailContent,
) {
  const section = mailElement("section", "detail-section suggestion-section");
  const heading = mailElement("div", "suggestion-heading");
  heading.append(mailElement("h3", "", "Bestehendem Vorgang zuordnen"));
  section.append(heading);

  const linkedIds = new Set(transaction.vorgangs_ids || []);
  const linkedItems = linkItems(suggestionsPayload, "vorgaenge")
    .filter((item) => linkedIds.has(item.id));
  const linkedList = mailElement("div", "mail-vorgang-list");
  if (linkedIds.size) {
    const byId = new Map(linkedItems.map((item) => [item.id, item]));
    for (const id of linkedIds) {
      const item = byId.get(id) || {id, label: id};
      const row = mailElement("div", "mail-vorgang-item");
      row.append(
        mailElement("strong", "", item.label || item.id),
        mailElement(
          "small",
          "",
          [
            item.type || item.vorgangstyp,
            formatStatus(item.status),
            item.date ? formatDateTimeOrDate(item.date) : "",
          ].filter(Boolean).join(" · "),
        ),
      );
      const openButton = mailElement(
        "button",
        "suggestion-open-action",
        "Öffnen",
      );
      openButton.type = "button";
      openButton.addEventListener("click", () => openVorgang(id));
      row.append(openButton);
      linkedList.append(row);
    }
  } else {
    linkedList.append(
      mailElement("p", "suggestion-empty", "Noch keinem Vorgang zugeordnet."),
    );
  }
  section.append(linkedList);

  const form = mailElement("form", "mail-vorgang-form");
  form.dataset.linkTransactionVorgang = transaction.transaktions_id;
  const searchLabel = mailElement("label", "suggestion-search");
  searchLabel.append(mailElement("span", "", "Suchen"));
  const search = document.createElement("input");
  search.type = "search";
  search.autocomplete = "off";
  search.placeholder = "Vorgänge durchsuchen";
  searchLabel.append(search);
  const list = mailElement("div", "suggestion-list");
  const candidates = linkItems(suggestionsPayload, "vorgaenge")
    .filter((item) => item?.id && !linkedIds.has(item.id));
  if (!candidates.length) {
    list.append(
      mailElement(
        "p",
        "suggestion-empty",
        "Keine weiteren Vorgänge gefunden.",
      ),
    );
  }
  for (const item of candidates) {
    const row = mailElement("div", "suggestion-row");
    row.classList.toggle("is-suggested", item.source === "suggestion");
    row.dataset.searchText = [
      item.label,
      item.id,
      item.reason,
      item.date,
      item.status,
      item.type,
      item.vorgangstyp,
      item.bezug,
    ].filter(Boolean).join(" ").toLocaleLowerCase("de-DE");
    const label = mailElement("label", "suggestion-choice");
    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "vorgangs_id";
    radio.value = item.id;
    const text = mailElement("span");
    text.append(
      mailElement("strong", "", item.label || item.id),
      mailElement(
        "small",
        "",
        [
          item.reason,
          item.type || item.vorgangstyp,
          formatStatus(item.status),
          item.date ? formatDateTimeOrDate(item.date) : "",
          item.amount ? currencyFormatter.format(Number(item.amount)) : "",
        ].filter(Boolean).join(" · "),
      ),
    );
    label.append(radio, text);
    row.append(label);
    list.append(row);
  }
  search.addEventListener("input", () => {
    const query = search.value.trim().toLocaleLowerCase("de-DE");
    let visible = 0;
    for (const row of list.querySelectorAll(".suggestion-row")) {
      row.hidden = Boolean(query) && !row.dataset.searchText.includes(query);
      if (!row.hidden) visible += 1;
    }
    queryEmpty.textContent = visible ? "" : "Keine Vorgänge zur Suche gefunden.";
  });
  const queryEmpty = mailElement("p", "suggestion-empty");
  const submit = mailElement(
    "button",
    "primary-action",
    "Zuordnung bestätigen",
  );
  submit.type = "submit";
  submit.disabled = !candidates.length;
  const status = mailElement("span", "save-state");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const selected = form.querySelector('input[name="vorgangs_id"]:checked');
    await submitVorgangAssignment({
      form,
      submit,
      status,
      selectedId: selected?.value || "",
      request: async () => {
        const response = await fetch(
        `/api/transactions/${encodeURIComponent(
          transaction.transaktions_id,
        )}/vorgaenge`,
        {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({vorgangs_id: selected.value}),
        },
        );
        await readResponse(response);
        state.vorgaengeLoaded = false;
      },
      onSaved: async () => {
        await Promise.all([
        loadTransactions(),
        loadTransactionWorkspace(
          transaction.transaktions_id,
          "Zuordnung gespeichert",
        ),
        ]);
        elements.detailDialogStatus.textContent = "Zuordnung gespeichert";
      },
    });
  });
  form.append(searchLabel, list, queryEmpty, submit, status);
  section.append(form);
  target.append(section);
}

function appendClassificationEditor(
  transaction,
  target = elements.detailContent,
) {
  const section = document.createElement("section");
  section.className = "detail-section classification-editor";
  const headingRow = document.createElement("div");
  headingRow.className = "classification-heading";
  const heading = document.createElement("h3");
  heading.textContent = "Klassifikation";
  const stateText = document.createElement("span");
  stateText.className = "save-state";
  stateText.textContent = "Änderungen werden automatisch gespeichert";
  headingRow.append(heading, stateText);

  const statusRow = document.createElement("div");
  statusRow.className = "classification-status";
  const statusLabel = document.createElement("span");
  statusLabel.className = "detail-label";
  statusLabel.textContent = "Klassifikationsstatus";
  let statusValue = classificationStatusBadge(
    transaction.klassifikationsstatus,
  );
  statusRow.append(statusLabel, statusValue);

  const form = document.createElement("form");
  form.className = "classification-form";
  form.addEventListener("submit", (event) => event.preventDefault());
  form.append(
    classificationField(
      "Transaktionstyp",
      "transaktionstyp",
      transaction.transaktionstyp,
    ),
    classificationField(
      "Oberkategorie",
      "oberkategorie",
      transaction.oberkategorie,
    ),
    classificationField(
      "Unterkategorie",
      "unterkategorie",
      transaction.unterkategorie,
    ),
    classificationField("Sphäre", "sphaere", transaction.sphaere),
    classificationField(
      "Fachliche Beschreibung",
      "fachliche_beschreibung",
      transaction.fachliche_beschreibung,
      true,
      true,
    ),
  );
  configureClassificationEditorFields(form);
  const budgetField = detailField(
    "Budget-ID",
    transaction.budget_id,
    true,
    true,
  );
  budgetField.classList.add("classification-budget");

  let saveTimer;
  let saving = false;
  let dirty = false;

  const scheduleSave = (delay = 450) => {
    dirty = true;
    clearTimeout(saveTimer);
    saveTimer = setTimeout(persist, delay);
  };

  const persist = async () => {
    if (saving || !dirty) {
      return;
    }
    dirty = false;
    saving = true;
    stateText.className = "save-state is-saving";
    stateText.textContent = "Wird gespeichert";
    const values = Object.fromEntries(
      [...form.elements]
        .filter((element) => element.name)
        .map((element) => [element.name, element.value]),
    );
    try {
      const response = await fetch(
        `/api/transactions/${encodeURIComponent(
          transaction.transaktions_id,
        )}/classification`,
        {
          method: "PATCH",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify(values),
        },
      );
      const payload = await readResponse(response);
      Object.assign(transaction, payload.transaction);
      const updatedStatus = classificationStatusBadge(
        transaction.klassifikationsstatus,
      );
      statusValue.replaceWith(updatedStatus);
      statusValue = updatedStatus;
      const budgetValue = budgetField.querySelector(".detail-value");
      setDetailValue(budgetValue, transaction.budget_id, true);
      updateVorgangDisplays(payload.vorgaenge);
      stateText.className = "save-state is-saved";
      stateText.textContent = "Gespeichert";
      state.vorgaengeLoaded = false;
      const refreshes = [loadTransactions()];
      if (!elements.vorgaengePanel.hidden) {
        refreshes.push(loadVorgaenge());
      }
      await Promise.all(refreshes);
    } catch (error) {
      stateText.className = "save-state is-error";
      stateText.textContent = "Speichern fehlgeschlagen";
      showError(error.message);
    } finally {
      saving = false;
      if (dirty) {
        clearTimeout(saveTimer);
        saveTimer = setTimeout(persist, 0);
      }
    }
  };

  for (const input of form.elements) {
    if (!input.name) {
      continue;
    }
    input.addEventListener("input", () => scheduleSave());
    input.addEventListener("blur", () => {
      if (dirty && !saving) {
        clearTimeout(saveTimer);
        persist();
      }
    });
  }

  section.append(headingRow, statusRow, form, budgetField);
  target.append(section);
}

function classificationField(label, name, value, wide = false, multiline = false) {
  const field = document.createElement("label");
  field.className =
    `classification-field${wide ? " is-wide" : ""}`;
  const fieldLabel = document.createElement("span");
  fieldLabel.className = "detail-label";
  fieldLabel.textContent = label;
  const input = document.createElement(
    multiline ? "textarea" : name === "sphaere" ? "select" : "input",
  );
  input.name = name;
  input.maxLength = 2000;
  input.autocomplete = "off";
  if (multiline) {
    input.rows = 3;
    input.value = value || "";
  } else if (name === "sphaere") {
    const current = document.createElement("option");
    current.value = value || "";
    current.textContent = value || "Nicht angegeben";
    input.append(current);
    input.value = value || "";
  } else {
    input.type = "text";
    input.value = value || "";
  }
  field.append(fieldLabel, input);
  return field;
}

function classificationStatusBadge(value) {
  const badge = document.createElement("span");
  badge.className = `classification-badge is-${value || "unklassifiziert"}`;
  badge.textContent = formatClassificationStatus(value);
  return badge;
}

function updateVorgangDisplays(vorgaenge) {
  for (const vorgang of vorgaenge) {
    for (const field of document.querySelectorAll(
      "[data-vorgang-id][data-vorgang-field]",
    )) {
      if (field.dataset.vorgangId !== vorgang.vorgangs_id) {
        continue;
      }
      let value = vorgang.vorgangstyp;
      if (field.dataset.vorgangField === "status") {
        value = formatStatus(vorgang.status);
      } else if (field.dataset.vorgangField === "aktualisiert_am") {
        value = formatDateTime(vorgang.aktualisiert_am);
      }
      setDetailValue(field.querySelector(".detail-value"), value);
    }
    if (elements.dialog.dataset.vorgangId === vorgang.vorgangs_id) {
      const count = Number(elements.dialog.dataset.vorgangTransactionCount);
      elements.detailTitle.textContent =
        vorgang.titel || vorgang.vorgangstyp || "Vorgang ohne Titel";
      elements.detailSubtitle.textContent =
        `${formatStatus(vorgang.status)} · ${count} ` +
        `${count === 1 ? "Transaktion" : "Transaktionen"}`;
    }
  }
}

function appendSplitEditor(transaction, target = elements.detailContent) {
  const originalAmount = Number(transaction.betrag_cent || 0);
  let splits = (transaction.splits || []).map((split) => ({...split}));
  let allowedVorgaenge = transaction.zulaessige_vorgaenge || [];
  const section = document.createElement("section");
  section.className = "detail-section split-editor";
  const headingRow = document.createElement("div");
  headingRow.className = "classification-heading";
  const heading = document.createElement("h3");
  heading.textContent = "Splits";
  const status = document.createElement("span");
  status.className = "save-state";
  status.textContent = splits.length
    ? "Split-Summe pruefen"
    : "Keine Splits erfasst";
  headingRow.append(heading, status);

  const form = document.createElement("form");
  form.className = "split-form";
  const formError = document.createElement("p");
  formError.className = "form-error";
  formError.hidden = true;
  formError.setAttribute("aria-live", "polite");
  const rows = document.createElement("div");
  rows.className = "split-rows";
  const summary = document.createElement("div");
  summary.className = "split-summary";
  summary.setAttribute("aria-live", "polite");
  const addButton = document.createElement("button");
  addButton.type = "button";
  addButton.className = "secondary-action";
  addButton.textContent = "Zeile hinzufuegen";
  const reloadButton = document.createElement("button");
  reloadButton.type = "button";
  reloadButton.className = "secondary-action";
  reloadButton.textContent = "Splits neu laden";
  const saveButton = document.createElement("button");
  saveButton.type = "submit";
  saveButton.className = "primary-action";
  saveButton.textContent = "Splits speichern";

  const readRows = () => [...rows.querySelectorAll("[data-split-row]")]
    .map((row, index) => {
      const amount = parseSplitAmountMinor(
        row.querySelector("[data-split-amount]").value,
        index + 1,
      );
      return {
        split_id: row.dataset.splitId || "",
        amount_minor: amount.value,
        amount_error: amount.error,
        description: row.querySelector("[data-split-description]").value,
        transaction_type: row.querySelector("[data-split-type]").value,
        top_category: row.querySelector("[data-split-top]").value,
        sub_category: row.querySelector("[data-split-sub]").value,
        sphere: row.querySelector("[data-split-sphere]").value,
        professional_description: row.querySelector(
          "[data-split-professional]",
        ).value,
        vorgangs_id: row.querySelector("[data-split-vorgang]").value,
      };
    });

  const updateSummary = () => {
    const current = readRows();
    const amountError = current.find((split) => split.amount_error);
    const sum = current.reduce(
      (total, split) => total + (split.amount_minor ?? 0),
      0,
    );
    const difference = originalAmount - sum;
    summary.replaceChildren(
      splitSummaryItem(
        "Originalbetrag",
        formatMinorAmount(originalAmount),
        "original",
      ),
      splitSummaryItem(
        "Split-Summe",
        formatMinorAmount(sum),
        "sum",
      ),
      splitSummaryItem(
        "Differenz",
        formatMinorAmount(difference),
        "difference",
      ),
    );
    const valid = current.length === 0 || difference === 0;
    summary.classList.toggle("is-balanced", valid);
    summary.classList.toggle("is-unbalanced", !valid);
    saveButton.disabled = Boolean(amountError);
    if (amountError) {
      formError.textContent = amountError.amount_error;
      formError.hidden = false;
      status.textContent = amountError.amount_error;
      elements.detailDialogStatus.textContent = amountError.amount_error;
    } else if (!current.length) {
      formError.hidden = true;
      status.textContent = "Speichern entfernt alle Splits";
      elements.detailDialogStatus.textContent = status.textContent;
    } else if (valid) {
      formError.hidden = true;
      status.textContent = "Split-Summe ausgeglichen";
      elements.detailDialogStatus.textContent = "";
    } else {
      formError.hidden = true;
      status.textContent = "Split-Summe nicht ausgeglichen";
      elements.detailDialogStatus.textContent = status.textContent;
    }
  };

  const addRow = (split = {}) => {
    const row = document.createElement("div");
    row.className = "split-row";
    row.dataset.splitRow = "true";
    row.dataset.splitId = split.split_id || "";
    row.append(
      splitInput(
        "Betrag (EUR)",
        formatMinorInput(split.amount_minor ?? split.betrag_cent),
        "amount",
      ),
      splitInput(
        "Beschreibung",
        split.description ?? split.beschreibung ?? "",
        "description",
      ),
      splitInput(
        "Transaktionstyp",
        split.transaction_type ?? split.transaktionstyp ?? "",
        "type",
      ),
      splitInput(
        "Oberkategorie",
        split.top_category ?? split.oberkategorie ?? "",
        "top",
      ),
      splitInput(
        "Unterkategorie",
        split.sub_category ?? split.unterkategorie ?? "",
        "sub",
      ),
      splitSphereField(split.sphere ?? split.sphaere ?? ""),
      splitInput(
        "Fachliche Beschreibung",
        split.professional_description ?? split.fachliche_beschreibung ?? "",
        "professional",
      ),
      splitVorgangField(split.vorgangs_id || "", allowedVorgaenge),
    );
    configureSplitClassificationFields(row);
    const meta = document.createElement("div");
    meta.className = "split-meta";
    meta.textContent = split.split_id
      ? [
          `ID ${split.split_id}`,
          `erstellt ${formatDateTime(split.created_at || split.erstellt_am)}`,
          `aktualisiert ${formatDateTime(
            split.updated_at || split.aktualisiert_am,
          )}`,
        ].join(" · ")
      : "Neue Split-Zeile";
    const removeButton = document.createElement("button");
    removeButton.type = "button";
    removeButton.className = "secondary-action split-remove";
    removeButton.textContent = "Entfernen";
    removeButton.addEventListener("click", () => {
      row.remove();
      updateSummary();
    });
    row.append(meta, removeButton);
    rows.append(row);
    updateSummary();
  };

  const renderRows = (nextSplits) => {
    splits = (nextSplits || []).map((split) => ({...split}));
    rows.replaceChildren();
    for (const split of splits) {
      addRow(split);
    }
    updateSummary();
  };

  addButton.addEventListener("click", () => {
    const current = readRows();
    const sum = current.reduce(
      (total, split) => total + (split.amount_minor ?? 0),
      0,
    );
    addRow({
      amount_minor: originalAmount - sum,
      description: "",
      transaction_type: transaction.transaktionstyp || "",
      top_category: transaction.oberkategorie || "",
      sub_category: transaction.unterkategorie || "",
      sphere: transaction.sphaere || "",
      professional_description: transaction.fachliche_beschreibung || "",
    });
  });
  reloadButton.addEventListener("click", async () => {
    reloadButton.disabled = true;
    status.className = "save-state is-saving";
    status.textContent = "Wird geladen";
    try {
      const response = await fetch(
        `/api/transactions/${encodeURIComponent(
          transaction.transaktions_id,
        )}/splits`,
      );
      const result = await readResponse(response);
      allowedVorgaenge = result.zulaessige_vorgaenge || [];
      transaction.zulaessige_vorgaenge = allowedVorgaenge;
      renderRows(result.splits || []);
      status.className = "save-state is-saved";
      status.textContent = "Splits geladen";
      elements.detailDialogStatus.textContent = "Splits geladen";
    } catch (error) {
      formError.textContent = error.message;
      formError.hidden = false;
      status.className = "save-state is-error";
      status.textContent = "Laden fehlgeschlagen";
      elements.detailDialogStatus.textContent = error.message;
      showError(error.message);
    } finally {
      reloadButton.disabled = false;
    }
  });
  rows.addEventListener("input", updateSummary);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const current = readRows();
    const amountError = current.find((split) => split.amount_error);
    if (amountError) {
      formError.textContent = amountError.amount_error;
      formError.hidden = false;
      status.className = "save-state is-error";
      status.textContent = "Eingabe pruefen";
      updateSummary();
      return;
    }
    const payload = {
      splits: current.map(({amount_error, ...split}) => split),
    };
    formError.hidden = true;
    saveButton.disabled = true;
    status.className = "save-state is-saving";
    status.textContent = "Wird gespeichert";
    try {
      const response = await fetch(
        `/api/transactions/${encodeURIComponent(
          transaction.transaktions_id,
        )}/splits`,
        {
          method: "PUT",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify(payload),
        },
      );
      const result = await readResponse(response);
      Object.assign(transaction, result.transaction);
      renderRows(transaction.splits || []);
      status.className = "save-state is-saved";
      status.textContent = "Gespeichert";
      elements.detailDialogStatus.textContent = "Splits gespeichert";
    } catch (error) {
      updateSummary();
      formError.textContent = error.message;
      formError.hidden = false;
      status.className = "save-state is-error";
      status.textContent = "Speichern fehlgeschlagen";
      elements.detailDialogStatus.textContent = error.message;
      showError(error.message);
    }
  });

  form.append(formError, rows, summary, addButton, reloadButton, saveButton);
  section.append(headingRow, form);
  renderRows(splits);
  target.append(section);
}

function splitSummaryItem(label, value, key) {
  const item = document.createElement("span");
  item.className = "split-summary-item";
  item.dataset.splitSummary = key;
  const itemLabel = document.createElement("span");
  itemLabel.className = "detail-label";
  itemLabel.textContent = label;
  const itemValue = document.createElement("strong");
  itemValue.textContent = value;
  item.append(itemLabel, itemValue);
  return item;
}

function splitInput(label, value, key) {
  const field = document.createElement("label");
  field.className = "split-field";
  const fieldLabel = document.createElement("span");
  fieldLabel.className = "detail-label";
  fieldLabel.textContent = label;
  const input = document.createElement("input");
  input.type = "text";
  input.value = value || "";
  input.autocomplete = "off";
  input.dataset[`split${key[0].toUpperCase()}${key.slice(1)}`] = "true";
  field.append(fieldLabel, input);
  return field;
}

function splitVorgangField(value, vorgaenge) {
  const wrapper = document.createElement("div");
  wrapper.className = "split-vorgang-field";
  const field = document.createElement("label");
  field.className = "split-field";
  const fieldLabel = document.createElement("span");
  fieldLabel.className = "detail-label";
  fieldLabel.textContent = "Vorgang";
  const select = document.createElement("select");
  select.dataset.splitVorgang = "true";
  const blank = document.createElement("option");
  blank.value = "";
  blank.textContent = "Nicht zugeordnet";
  select.append(blank);
  for (const vorgang of vorgaenge) {
    const option = document.createElement("option");
    option.value = vorgang.vorgangs_id;
    const title = vorgang.titel || vorgang.vorgangs_id;
    option.textContent = `${title} · ${formatStatus(vorgang.status)}`;
    option.title = vorgang.vorgangs_id;
    select.append(option);
  }
  select.value = [...select.options].some((option) => option.value === value)
    ? value
    : "";
  const hint = document.createElement("p");
  hint.className = "split-vorgang-hint";
  hint.setAttribute("aria-live", "polite");
  const updateHint = () => {
    const selected = vorgaenge.find(
      (vorgang) => vorgang.vorgangs_id === select.value,
    );
    if (!selected) {
      hint.textContent = "Kein Vorgang zugeordnet.";
      return;
    }
    const belege = selected.belege || [];
    const belegText = belege.length
      ? belege.map((beleg) => beleg.dateiname || beleg.beleg_id).join(", ")
      : "Keine Belege vorhanden";
    hint.textContent = `Status: ${formatStatus(selected.status)} · Belege des Vorgangs: ${belegText}`;
  };
  select.addEventListener("change", updateHint);
  field.append(fieldLabel, select);
  wrapper.append(field, hint);
  updateHint();
  return wrapper;
}

function splitSphereField(value) {
  const field = document.createElement("label");
  field.className = "split-field";
  const fieldLabel = document.createElement("span");
  fieldLabel.className = "detail-label";
  fieldLabel.textContent = "Sphaere";
  const select = document.createElement("select");
  select.dataset.splitSphere = "true";
  const blank = document.createElement("option");
  blank.value = "";
  blank.textContent = "Nicht angegeben";
  select.append(blank);
  for (const sphere of state.classificationOptions.spheres || []) {
    const option = document.createElement("option");
    option.value = sphere;
    option.textContent = sphere;
    select.append(option);
  }
  if (value && ![...select.options].some((option) => option.value === value)) {
    const existing = document.createElement("option");
    existing.value = value;
    existing.textContent = value;
    select.append(existing);
  }
  select.value = [...select.options].some((option) => option.value === value)
    ? value
    : "";
  field.append(fieldLabel, select);
  return field;
}

function configureSplitClassificationFields(row) {
  const transactionType = row.querySelector("[data-split-type]");
  const topCategory = row.querySelector("[data-split-top]");
  const subCategory = row.querySelector("[data-split-sub]");
  const sphere = row.querySelector("[data-split-sphere]");
  if (!transactionType || !topCategory || !subCategory || !sphere) {
    return;
  }

  const createDatalist = (input, name, values) => {
    const datalist = document.createElement("datalist");
    datalist.dataset.classificationOptions = name;
    datalist.id = `split-${name}-${ruleDatalistCounter += 1}`;
    for (const value of values) {
      const option = document.createElement("option");
      option.value = value;
      datalist.append(option);
    }
    row.append(datalist);
    input.setAttribute("list", datalist.id);
    return datalist;
  };

  createDatalist(
    transactionType,
    "transaction-types",
    state.classificationOptions.transaction_types || [],
  );
  createDatalist(
    topCategory,
    "top-categories",
    state.classificationOptions.top_categories || [],
  );
  const subcategoryDatalist = createDatalist(
    subCategory,
    "sub-categories",
    [],
  );

  const subcategories = new Map(
    (state.classificationOptions.sub_categories || []).map((entry) => [
      entry.top_category.toLocaleLowerCase("de-DE"),
      entry.values,
    ]),
  );
  const sphereDefaults = new Map(
    (state.classificationOptions.sphere_defaults || []).map((entry) => [
      [
        entry.top_category.toLocaleLowerCase("de-DE"),
        entry.sub_category.toLocaleLowerCase("de-DE"),
      ].join("\u0000"),
      entry.sphere,
    ]),
  );

  const refreshSubcategories = () => {
    const topValue = topCategory.value.trim();
    subCategory.disabled = !topValue;
    subcategoryDatalist.replaceChildren();
    const values = subcategories.get(
      topValue.toLocaleLowerCase("de-DE"),
    ) || [];
    for (const value of values) {
      const option = document.createElement("option");
      option.value = value;
      subcategoryDatalist.append(option);
    }
  };

  const applySphereDefault = () => {
    const topValue = topCategory.value.trim();
    const subValue = subCategory.value.trim();
    if (sphere.value || !topValue || !subValue) {
      return;
    }
    const preferred = sphereDefaults.get(
      [
        topValue.toLocaleLowerCase("de-DE"),
        subValue.toLocaleLowerCase("de-DE"),
      ].join("\u0000"),
    );
    if (preferred) {
      sphere.value = preferred;
    }
  };

  topCategory.addEventListener("input", () => {
    refreshSubcategories();
    applySphereDefault();
  });
  topCategory.addEventListener("change", () => {
    refreshSubcategories();
    applySphereDefault();
  });
  subCategory.addEventListener("input", applySphereDefault);
  subCategory.addEventListener("change", applySphereDefault);
  refreshSubcategories();
}

function parseSplitAmountMinor(value, index) {
  const raw = String(value ?? "").trim();
  if (!raw) {
    return {
      value: null,
      error: `Split ${index} braucht einen Betrag in Euro.`,
    };
  }
  const match = raw.replace(",", ".").match(/^(-?)(\d+)(?:\.(\d{1,2}))?$/);
  if (!match) {
    return {
      value: null,
      error: `Split ${index} braucht einen Euro-Betrag mit maximal zwei Nachkommastellen.`,
    };
  }
  const sign = match[1] === "-" ? -1 : 1;
  const euros = Number.parseInt(match[2], 10);
  const cents = Number.parseInt((match[3] || "").padEnd(2, "0"), 10) || 0;
  return {value: sign * ((euros * 100) + cents), error: ""};
}

function formatMinorInput(value) {
  if (value === null || value === undefined || value === "") {
    return "";
  }
  const sign = Number(value) < 0 ? "-" : "";
  const absolute = Math.abs(Number(value));
  const euros = Math.trunc(absolute / 100);
  const cents = String(absolute % 100).padStart(2, "0");
  return `${sign}${euros},${cents}`;
}

function formatMinorAmount(value) {
  return currencyFormatter.format(Number(value || 0) / 100);
}

function appendDetailSection(
  title,
  fields,
  target = elements.detailContent,
) {
  const section = document.createElement("section");
  section.className = "detail-section";
  const heading = document.createElement("h3");
  heading.textContent = title;
  const grid = document.createElement("div");
  grid.className = "detail-grid";
  grid.append(...fields);
  section.append(heading, grid);
  target.append(section);
}

function detailField(
  label,
  value,
  wide = false,
  monospace = false,
  vorgangsId = "",
  vorgangField = "",
) {
  const field = document.createElement("div");
  field.className = `detail-field${wide ? " is-wide" : ""}`;
  if (vorgangsId) {
    field.dataset.vorgangId = vorgangsId;
    field.dataset.vorgangField = vorgangField;
  }
  const fieldLabel = document.createElement("span");
  fieldLabel.className = "detail-label";
  fieldLabel.textContent = label;
  const fieldValue = document.createElement("div");
  fieldValue.className =
    `detail-value${monospace ? " is-monospace" : ""}`;
  setDetailValue(fieldValue, value);
  field.append(fieldLabel, fieldValue);
  return field;
}

function setDetailValue(element, value) {
  const empty = value === null || value === undefined || value === "";
  element.classList.toggle("is-empty", empty);
  element.textContent = empty ? "Nicht angegeben" : String(value);
}

function appendSourceSection(sources, target = elements.detailContent) {
  const section = document.createElement("section");
  section.className = "detail-section";
  const heading = document.createElement("h3");
  heading.textContent = "Importquellen";
  const list = document.createElement("div");
  list.className = "source-list";
  if (!sources.length) {
    list.append(detailField("Quelle", ""));
  } else {
    for (const source of sources) {
      const card = document.createElement("div");
      card.className = "source-card";
      const filename = document.createElement("span");
      filename.textContent = source.dateiname;
      filename.title = source.dateiname;
      const run = document.createElement("span");
      run.textContent = source.exportlauf;
      run.title = source.exportlauf;
      const row = document.createElement("span");
      row.textContent = `Zeile ${source.zeilennummer}`;
      card.append(filename, run, row);
      list.append(card);
    }
  }
  section.append(heading, list);
  target.append(section);
}

function appendRawDataSection(rawData, target = elements.detailContent) {
  const fields = Object.entries(rawData || {}).map(([label, value]) =>
    detailField(label, value),
  );
  appendDetailSection(
    "Originale Bankfelder",
    fields.length ? fields : [detailField("Rohdaten", "")],
    target,
  );
}

async function loadBudgets() {
  elements.budgetLoading.hidden = false;
  elements.budgetTable.hidden = true;
  elements.budgetEmpty.hidden = true;
  try {
    const response = await fetch("/api/budgets");
    const payload = await readResponse(response);
    renderBudgets(payload.budgets);
    state.budgetsLoaded = true;
  } catch (error) {
    showError(error.message);
  } finally {
    elements.budgetLoading.hidden = true;
  }
}

function renderBudgets(budgets) {
  elements.budgetRows.replaceChildren();
  for (const budget of budgets) {
    const row = document.createElement("tr");
    row.append(
      tableCell(budget.saison, "account-cell"),
      tableCell(budget.oberkategorie),
      tableCell(budget.unterkategorie),
      budgetAmountCell(budget.einnahmen),
      budgetAmountCell(budget.ausgaben),
      budgetAmountCell(budget.budget),
    );
    elements.budgetRows.append(row);
  }
  elements.budgetCount.textContent = integerFormatter.format(budgets.length);
  elements.budgetEmpty.hidden = budgets.length > 0;
  elements.budgetTable.hidden = budgets.length === 0;
}

function budgetAmountCell(value) {
  const cell = document.createElement("td");
  cell.className = "amount-column";
  cell.textContent = currencyFormatter.format(Number(value));
  return cell;
}

function renderBalances(summary) {
  const total = summary.kontostand_gesamt;
  elements.totalBalance.textContent =
    total === null ? "Nicht verfügbar" : currencyFormatter.format(Number(total));
  elements.totalBalanceLabel.textContent = summary.vollstaendig
    ? "Kontostand gesamt"
    : "Bekannter Gesamtstand";
  if (summary.vollstaendig) {
    elements.totalBalanceNote.textContent =
      `Vollständig über ${summary.konten.length} Konten`;
  } else if (summary.fehlende_konten.length) {
    elements.totalBalanceNote.textContent =
      `Teilstand · ohne ${summary.fehlende_konten.join(", ")}`;
  } else {
    elements.totalBalanceNote.textContent = "Kein Kontostand verfügbar";
  }

  elements.accountBalances.replaceChildren();
  const accountSelect = elements.balanceCorrectionForm.elements.account_id;
  const selectedAccount = accountSelect.value;
  accountSelect.replaceChildren(new Option("Konto auswählen", ""));
  for (const account of summary.konten) {
    const card = document.createElement("div");
    card.className = "balance-card";
    const label = document.createElement("span");
    label.className = "balance-label";
    label.textContent = account.kontoname;
    const value = document.createElement("strong");
    value.textContent =
      account.kontostand === null
        ? "Nicht verfügbar"
        : currencyFormatter.format(Number(account.kontostand));
    const note = document.createElement("span");
    note.className = "balance-note";
    note.textContent = account.stand_vom
      ? `Stand ${formatDate(account.stand_vom)}`
      : "CSV enthält keinen Kontostand";
    card.append(label, value, note);
    elements.accountBalances.append(card);

    const provider = account.provider ? `${account.provider} · ` : "";
    const number = account.kontonummer ? ` · ${account.kontonummer}` : "";
    accountSelect.append(new Option(
      `${provider}${account.kontoname}${number}`,
      account.account_id,
    ));
  }
  accountSelect.value = selectedAccount;
}

async function loadBalanceCorrections() {
  elements.balanceCorrectionLoading.hidden = false;
  elements.balanceCorrectionEmpty.hidden = true;
  try {
    const response = await fetch("/api/balance-corrections");
    const payload = await readResponse(response);
    renderBalanceCorrections(payload.corrections || []);
  } catch (error) {
    elements.balanceCorrectionStatus.className = "is-error";
    elements.balanceCorrectionStatus.textContent = error.message;
  } finally {
    elements.balanceCorrectionLoading.hidden = true;
  }
}

function renderBalanceCorrections(corrections) {
  elements.balanceCorrectionList.replaceChildren();
  elements.balanceCorrectionCount.textContent =
    `${integerFormatter.format(corrections.length)} ${corrections.length === 1 ? "Korrektur" : "Korrekturen"}`;
  elements.balanceCorrectionEmpty.hidden = corrections.length > 0;
  for (const correction of corrections) {
    const card = document.createElement("article");
    card.className = "balance-correction-card";
    const heading = document.createElement("div");
    heading.className = "balance-correction-card-heading";
    const account = document.createElement("strong");
    account.textContent = correction.account_name || correction.account_id;
    const amount = document.createElement("strong");
    amount.className = correction.balance_minor < 0 ? "is-negative" : "is-positive";
    amount.textContent = currencyFormatter.format(correction.balance_minor / 100);
    heading.append(account, amount);
    const accountDetail = document.createElement("p");
    accountDetail.textContent = [correction.provider, correction.account_number]
      .filter(Boolean).join(" · ");
    const details = document.createElement("dl");
    for (const [label, value] of [
      ["Stichtag", formatDate(correction.balance_as_of)],
      ["Begründung", correction.reason],
      ["Erstellt", formatDateTime(correction.created_at)],
    ]) {
      const term = document.createElement("dt");
      term.textContent = label;
      const description = document.createElement("dd");
      description.textContent = value;
      details.append(term, description);
    }
    const notice = document.createElement("p");
    notice.className = "balance-correction-manual-notice";
    notice.textContent = "Manuell geprüft · Originaltransaktionen unverändert";
    card.append(heading, accountDetail, details, notice);
    elements.balanceCorrectionList.append(card);
  }
}

async function saveBalanceCorrection(event) {
  event.preventDefault();
  const form = elements.balanceCorrectionForm;
  elements.balanceCorrectionStatus.className = "";
  if (!form.reportValidity()) {
    elements.balanceCorrectionStatus.textContent = "Bitte alle Pflichtfelder prüfen.";
    return;
  }
  const rawAmount = form.elements.balance_minor.value.trim();
  if (!/^-?\d+$/.test(rawAmount) || !Number.isSafeInteger(Number(rawAmount))) {
    elements.balanceCorrectionStatus.className = "is-error";
    elements.balanceCorrectionStatus.textContent = "Der Saldo muss ein ganzzahliger Centbetrag sein.";
    return;
  }
  const submit = form.querySelector('button[type="submit"]');
  submit.disabled = true;
  elements.balanceCorrectionStatus.textContent = "Korrektur wird gespeichert";
  try {
    const response = await fetch("/api/balance-corrections", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        account_id: form.elements.account_id.value,
        balance_minor: Number(rawAmount),
        balance_as_of: form.elements.balance_as_of.value,
        reason: form.elements.reason.value.trim(),
      }),
    });
    await readResponse(response);
    form.reset();
    elements.balanceCorrectionStatus.className = "is-success";
    elements.balanceCorrectionStatus.textContent = "Korrektur wurde angelegt.";
    await loadBalanceCorrections();
  } catch (error) {
    elements.balanceCorrectionStatus.className = "is-error";
    elements.balanceCorrectionStatus.textContent = error.message;
  } finally {
    submit.disabled = false;
  }
}

function amountBadge(value) {
  const amount = Number(value);
  const badge = document.createElement("span");
  badge.className =
    `amount-value ${amount < 0 ? "is-negative" : "is-positive"}`;
  badge.textContent = currencyFormatter.format(amount);
  return badge;
}

function createLoadingBlock() {
  const loading = document.createElement("div");
  loading.className = "loading-state";
  const spinner = document.createElement("span");
  spinner.className = "spinner";
  spinner.setAttribute("aria-hidden", "true");
  loading.append(spinner, "Details werden geladen");
  return loading;
}

function formatDate(value) {
  if (!value) {
    return "";
  }
  const parts = String(value).slice(0, 10).split("-");
  if (parts.length !== 3) {
    return value;
  }
  return `${parts[2]}.${parts[1]}.${parts[0]}`;
}

function formatChartDate(value) {
  return new Intl.DateTimeFormat("de-DE", {
    day: "2-digit",
    month: "2-digit",
    year: "2-digit",
  }).format(value);
}

function formatDateTime(value) {
  if (!value) {
    return "";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return new Intl.DateTimeFormat("de-DE", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

function formatDateTimeOrDate(value) {
  const raw = String(value || "");
  if (/^\d{4}-\d{2}-\d{2}$/.test(raw)) {
    return formatDate(raw);
  }
  return formatDateTime(raw);
}

function apiDateTimeToLocalInput(value) {
  if (!value) {
    return "";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return String(value).slice(0, 16);
  }
  const local = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
  return local.toISOString().slice(0, 16);
}

function localDateTimeToApiValue(value) {
  if (!value) {
    return "";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toISOString();
}

function formatOptionalCurrency(value) {
  if (value === null || value === undefined || value === "") {
    return "";
  }
  return currencyFormatter.format(Number(value));
}

function applyDateFilter() {
  if (!elements.dateFrom.value || !elements.dateTo.value) {
    return;
  }
  if (elements.dateFrom.value > elements.dateTo.value) {
    showError("Das Von-Datum darf nicht nach dem Bis-Datum liegen.");
    return;
  }
  state.dateFrom = elements.dateFrom.value;
  state.dateTo = elements.dateTo.value;
  loadTransactions();
}

function setDefaultPeriod() {
  const end = new Date();
  const start = subtractMonths(end, 3);
  state.dateFrom = toDateInputValue(start);
  state.dateTo = toDateInputValue(end);
  elements.dateFrom.value = state.dateFrom;
  elements.dateTo.value = state.dateTo;
}

async function setMaximumPeriod() {
  elements.maxPeriod.disabled = true;
  try {
    const response = await fetch("/api/transactions/period");
    const payload = await readResponse(response);
    if (!payload.available || !payload.date_from || !payload.date_to) {
      showError("Es sind noch keine Transaktionen mit Datum vorhanden.");
      return;
    }
    state.dateFrom = payload.date_from;
    state.dateTo = payload.date_to;
    elements.dateFrom.value = state.dateFrom;
    elements.dateTo.value = state.dateTo;
    await loadTransactions();
  } catch (error) {
    showError(error.message);
  } finally {
    elements.maxPeriod.disabled = false;
  }
}

function setDefaultHistoryPeriod() {
  const end = new Date();
  const start = subtractMonths(end, 3);
  elements.historyDateFrom.value = toDateInputValue(start);
  elements.historyDateTo.value = toDateInputValue(end);
}

function subtractMonths(value, months) {
  const result = new Date(value);
  const originalDay = result.getDate();
  result.setDate(1);
  result.setMonth(result.getMonth() - months);
  const lastDay = new Date(
    result.getFullYear(),
    result.getMonth() + 1,
    0,
  ).getDate();
  result.setDate(Math.min(originalDay, lastDay));
  return result;
}

function toDateInputValue(value) {
  const year = value.getFullYear();
  const month = String(value.getMonth() + 1).padStart(2, "0");
  const day = String(value.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function joinValues(values) {
  return Array.isArray(values) && values.length ? values.join(", ") : "";
}

function formatStatus(value) {
  const labels = {
    abgeschlossen: "Abgeschlossen",
    in_bearbeitung: "In Bearbeitung",
  };
  return labels[value] || value || "Nicht angegeben";
}

function formatClassificationStatus(value) {
  const labels = {
    unklassifiziert: "Unklassifiziert",
    unvollstaendig_klassifiziert: "Unvollständig klassifiziert",
    vollstaendig_klassifiziert: "Vollständig klassifiziert",
  };
  return labels[value] || value || "Unklassifiziert";
}

async function readResponse(response) {
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.error || "Die Anfrage ist fehlgeschlagen.");
  }
  return payload;
}

function showError(message) {
  clearTimeout(toastTimer);
  elements.errorToast.textContent = message;
  elements.errorToast.hidden = false;
  toastTimer = setTimeout(() => {
    elements.errorToast.hidden = true;
  }, 5000);
}

updateSortIndicators();
setDefaultPeriod();
setDefaultHistoryPeriod();
loadOverview();
loadTransactions();
loadBalanceCorrections();
loadRefreshStatus();

