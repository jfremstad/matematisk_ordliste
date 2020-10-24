$.fn.bootstrapTable.locales["nb-NO"] = {
  formatCopyRows() {
    return "Kopier rader";
  },
  formatPrint() {
    return "Print";
  },
  formatLoadingMessage() {
    return "Oppdaterer...";
  },
  formatRecordsPerPage(pageNumber) {
    return `${pageNumber} innslag per side`;
  },
  formatShowingRows(pageFrom, pageTo, totalRows, totalNotFiltered) {
    if (
      totalNotFiltered !== undefined &&
      totalNotFiltered > 0 &&
      totalNotFiltered > totalRows
    ) {
      return `Viser ${pageFrom} til ${pageTo} av ${totalRows} rader (ut av ${totalNotFiltered} rader)`;
    }

    return `Viser rad ${pageFrom}-${pageTo} av ${totalRows} rader`;
  },
  formatSRPaginationPreText() {
    return "forrige side";
  },
  formatSRPaginationPageText(page) {
    return `til side ${page}`;
  },
  formatSRPaginationNextText() {
    return "neste side";
  },
  formatDetailPagination(totalRows) {
    return `Viser ${totalRows} rader`;
  },
  formatClearSearch() {
    return "Clear Search";
  },
  formatSearch() {
    return "Søk";
  },
  formatNoMatches() {
    return "Søket ga ingen resultater";
  },
  formatPaginationSwitch() {
    return "Hide/Show pagination";
  },
  formatPaginationSwitchDown() {
    return "Show pagination";
  },
  formatPaginationSwitchUp() {
    return "Hide pagination";
  },
  formatRefresh() {
    return "Oppdater";
  },
  formatToggle() {
    return "Endre";
  },
  formatToggleOn() {
    return "Show card view";
  },
  formatToggleOff() {
    return "Hide card view";
  },
  formatColumns() {
    return "Kolonner";
  },
  formatColumnsToggleAll() {
    return "Toggle all";
  },
  formatFullscreen() {
    return "Fullscreen";
  },
  formatAllRows() {
    return "All";
  },
  formatAutoRefresh() {
    return "Auto Refresh";
  },
  formatExport() {
    return "Export data";
  },
  formatJumpTo() {
    return "GO";
  },
  formatAdvancedSearch() {
    return "Advanced search";
  },
  formatAdvancedCloseButton() {
    return "Close";
  },
  formatFilterControlSwitch() {
    return "Hide/Show controls";
  },
  formatFilterControlSwitchHide() {
    return "Hide controls";
  },
  formatFilterControlSwitchShow() {
    return "Show controls";
  },
};

$.extend($.fn.bootstrapTable.defaults, $.fn.bootstrapTable.locales["nb-NO"]);
