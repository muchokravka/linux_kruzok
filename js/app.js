(function () {
  "use strict";

  var lessonIds = null;
  var ticking = false;
  var SCROLL_OFFSET = 92;
  var ACTIVE_TOLERANCE = 4;

  function collectLessons() {
    var lessons = document.querySelectorAll(".lesson");
    lessonIds = [];
    lessons.forEach(function (l) {
      lessonIds.push(l.id);
    });
  }

  function highlightLesson(target) {
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
  }

  function updateActive() {
    var hash = window.location.hash.replace("#", "");
    var target = hash || lessonIds[0] || "";

    highlightLesson(target);

    if (target) {
      var el = document.getElementById(target);
      if (el) {
        var top = el.getBoundingClientRect().top + window.scrollY - SCROLL_OFFSET;
        window.scrollTo({ top: top, behavior: "smooth" });
      }
    }
  }

  function lessonFromScroll() {
    var sections = document.querySelectorAll(".lesson");
    if (!sections.length) return null;

    var offset = SCROLL_OFFSET;
    var current = sections[0].id;

    var threshold = offset + ACTIVE_TOLERANCE;

    for (var i = 0; i < sections.length; i++) {
      var top = sections[i].getBoundingClientRect().top;
      if (top <= threshold) {
        current = sections[i].id;
      } else {
        break;
      }
    }

    var maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    if (window.scrollY >= maxScroll - 4) {
      current = sections[sections.length - 1].id;
    }

    return current;
  }

  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      var id = lessonFromScroll();
      if (id) highlightLesson(id);
      ticking = false;
    });
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
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();