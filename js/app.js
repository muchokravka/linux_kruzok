(function () {
  "use strict";

  var lessonIds = null;

  function collectLessons() {
    var lessons = document.querySelectorAll(".lesson");
    lessonIds = [];
    lessons.forEach(function (l) {
      lessonIds.push(l.id);
    });
  }

  function updateActive() {
    var hash = window.location.hash.replace("#", "");
    var target = hash || lessonIds[0] || "";

    var links = document.querySelectorAll(".timeline-group .lessons a");
    var activeLesson = null;

    links.forEach(function (a) {
      a.classList.remove("active");
      if (a.getAttribute("href") === "#" + target) {
        a.classList.add("active");
        activeLesson = a;
      }
    });

    var current = document.getElementById("current-lesson");
    if (current && activeLesson) {
      current.textContent = activeLesson.textContent.trim();
    }

    if (activeLesson) {
      var group = activeLesson.closest(".timeline-group");
      if (group) {
        group.classList.add("open");
      }
    }

    if (target) {
      var el = document.getElementById(target);
      if (el) {
        el.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }
  }

  function initAccordions() {
    document.querySelectorAll(".group-label").forEach(function (label) {
      label.addEventListener("click", function () {
        var group = label.closest(".timeline-group");
        group.classList.toggle("open");
      });
    });
  }

  function initHamburger() {
    var hamburger = document.getElementById("hamburger");
    var sidebar = document.getElementById("sidebar");
    var backdrop = document.getElementById("backdrop");
    if (!hamburger || !sidebar) return;

    function close() {
      sidebar.classList.remove("open");
      if (backdrop) backdrop.style.display = "none";
    }

    hamburger.addEventListener("click", function () {
      var isOpen = sidebar.classList.toggle("open");
      if (backdrop) backdrop.style.display = isOpen ? "block" : "none";
    });

    if (backdrop) {
      backdrop.addEventListener("click", close);
    }

    sidebar.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", close);
    });
  }

  function init() {
    collectLessons();
    initAccordions();
    initHamburger();
    updateActive();

    window.addEventListener("hashchange", updateActive);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
