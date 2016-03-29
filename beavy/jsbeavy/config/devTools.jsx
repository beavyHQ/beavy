import React from 'react'
import { render } from 'react-dom'

// Exported from redux-devtools
import { createDevTools } from 'redux-devtools'

// Monitors are separate packages, and you can make a custom one
import LogMonitor from 'redux-devtools-log-monitor'
import DockMonitor from 'redux-devtools-dock-monitor'
import SliderMonitor from 'redux-slider-monitor'

// createDevTools takes a monitor and produces a DevTools component
const DevTools = createDevTools(
  <DockMonitor toggleVisibilityKey='ctrl-h'
               changePositionKey='ctrl-q'
               defaultIsVisible
               defaultSize={1.0}
               changeMonitorKey='ctrl-m'>
    <LogMonitor />
    <SliderMonitor />
  </DockMonitor>
)

function showDevTools (store) {
  const popup = window.open(null, 'Redux DevTools', 'menubar=no,location=no,resizable=no,scrollbars=no,status=no,width=400px')
  // Reload in case it already exists
  popup.location.reload()

  setTimeout(() => {
    popup.document.write('<div id="react-devtools-root"></div>')
    render(
      <DevTools store={store} />,
      popup.document.getElementById('react-devtools-root')
    )
  }, 10)
}

export { DevTools, showDevTools }
