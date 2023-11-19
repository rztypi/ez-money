/* Theme toggler */
(() => {
  "use strict"

  const getStoredTheme = () => localStorage.getItem('theme')
  const setStoredTheme = theme => localStorage.setItem('theme', theme)

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme()
    if (storedTheme) {
      return storedTheme
    }

    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }

  const setTheme = theme => {
    if (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.setAttribute('data-bs-theme', 'dark')
    } else {
      document.documentElement.setAttribute('data-bs-theme', theme)
    }
  }
  setTheme(getPreferredTheme())

  const showActiveTheme = (theme, focus = false) => {
    const themeSwitcher = document.getElementById("themeSwitch")

    if (!themeSwitcher) {
      return
    }

    const icon = themeSwitcher.querySelector("i")
    if (theme === "dark") {
      icon.classList.remove("bi-sun")
      icon.classList.add("bi-moon-fill")
    } else {
      icon.classList.remove("bi-moon-fill")
      icon.classList.add("bi-sun")
    }

    if (focus) {
      themeSwitcher.focus()
    }
  }

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const storedTheme = getStoredTheme()
    if (storedTheme !== 'light' && storedTheme !== 'dark') {
      setTheme(getPreferredTheme())
    }
  })

  window.addEventListener('DOMContentLoaded', () => {
    showActiveTheme(getPreferredTheme())

    document.getElementById("themeSwitch").addEventListener("click", () => {
      const theme = (getPreferredTheme() === "dark") ? "light" : "dark"
      setStoredTheme(theme)
      setTheme(theme)
      showActiveTheme(theme)
    })
  })
})();


/* Graph visibility */
(() => {
  "use strict"

  const getStoredGraphVisibility = () => localStorage.getItem("graphVisibility")
  const setStoredGraphVisibility = (visibility) => localStorage.setItem("graphVisibility", visibility)

  const getPreferredVisibility = () => {
    const visibility = getStoredGraphVisibility()
    if (visibility) {
      return visibility
    }

    return "show"
  }

  const setGraphVisibility = (visibility) => {
    const graph = document.getElementById("barGraph")
    if (!graph) {
      return
    }

    if (visibility === "show") {
      graph.classList.remove("d-none")
    } else if (visibility === "hide") {
      graph.classList.add("d-none")
    }
  }

  window.addEventListener("DOMContentLoaded", () => {
    setGraphVisibility(getPreferredVisibility())

    const graphSwitch = document.getElementById("graphSwitch")
    if (!graphSwitch) {
      return
    }
    graphSwitch.checked = (getPreferredVisibility() === "show") ? true : false
    graphSwitch.addEventListener("click", (evt) => {
      let visibility = (evt.target.checked) ? "show" : "hide"
      setStoredGraphVisibility(visibility)
      setGraphVisibility(visibility)
    })
  })
})()