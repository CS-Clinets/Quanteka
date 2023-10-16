// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.
var report;
var reportLoadConfig;
var models;
var reportContainer = $("#report-container").get(0);
$(function () {
  // Initialize iframe for embedding report
  powerbi.bootstrap(reportContainer, { type: "report" });

  // Get models. models contains enums that can be used.
  models = window["powerbi-client"].models;

  // We give All permissions to demonstrate switching between View and Edit mode and saving report.
  let permissions = models.Permissions.All;

  // Read embed type from radio
  let tokenType;

  reportLoadConfig = {
    type: "report",
    tokenType: tokenType == "0" ? models.TokenType.Aad : models.TokenType.Embed,
    permissions: permissions,
    settings: {
      panes: {
        filters: {
          visible: false,
        },
      },
      layoutType: models.LayoutType.MobilePortrait,
    },
  };

  function getReportId() {
    let url = document.location.href;
    return url.split("reportId=")[1];
  }

  $.ajax({
    type: "GET",
    url: `/getembedinfo?r_id=${getReportId()}`,
    dataType: "json",
    success: function (data) {
      let embedData = JSON.parse(data);
      reportLoadConfig.accessToken = embedData.accessToken;

      // You can embed different reports as per your need
      reportLoadConfig.embedUrl = embedData.reportConfig[0].embedUrl;

      // Use the token expiry to regenerate Embed token for seamless end user experience
      // Refer https://aka.ms/RefreshEmbedToken
      reportLoadConfig.tokenExpiry = embedData.tokenExpiry;
      reportLoadConfig.id = embedData.reportConfig[0].reportId;
      reportLoadConfig.pageName = embedData.reportConfig[0].reportName;

      // Embed Power BI report when Access token and Embed URL are available
      report = powerbi.embed(reportContainer, reportLoadConfig);

      // Triggers when a report schema is successfully loaded
      report.on("loaded", function () {
        console.log("Report load successful");
      });

      // Triggers when a report is successfully embedded in UI
      report.on("rendered", function () {
        console.log("Report render successful");
      });
      setLayout();

      // Clear any other error handler event
      report.off("error");

      // Below patch of code is for handling errors that occur during embedding
      report.on("error", function (event) {
        var errorMsg = event.detail;

        // Use errorMsg variable to log error in any destination of choice
        console.error(errorMsg);
        return;
      });
    },
    error: function (err) {
      // Show error container
      var errorContainer = $(".error-container");
      $(".embed-container").hide();
      errorContainer.show();

      // Format error message
      var errMessageHtml =
        "<strong> Error Details: </strong> <br/>" +
        $.parseJSON(err.responseText)["errorMsg"];
      errMessageHtml = errMessageHtml.split("\n").join("<br/>");

      // Show error message on UI
      errorContainer.html(errMessageHtml);
    },
  });
});

function setLayout() {
  if ($(window).width() < 960) {
    reportLoadConfig.settings.layoutType = models.LayoutType.MobilePortrait;
    powerbi.reset(reportContainer);
    report = powerbi.embed(reportContainer, reportLoadConfig);
  } else if ($(window).width() > 960) {
    reportLoadConfig.settings.layoutType = null;
    powerbi.reset(reportContainer);
    report = powerbi.embed(reportContainer, reportLoadConfig);
  }
}

window.addEventListener("resize", () => setLayout());
