import React from 'react';
import config from 'config/config';

export function createConstants (...constants) {
  return constants.reduce((acc, constant) => {
    acc[constant] = constant;
    return acc;
  }, {});
}

export function getStoreEntity(state, item){
  return state.entities[item.type][item.id];
}

function makePrefixUrlMaker(prefix){
  if (prefix.slice(-1) != '/') prefix += "/";
  return (function makeUrl(inp){
    let url = prefix + inp;
    if (url.slice(-1) != '/'){
      url += "/"
    }
    return url;
  })
}

export const make_url = function(cfg){
  const urlMakers = {};
  for (var key in cfg){
    if (cfg.hasOwnProperty(key) && key.slice(-4) === "_URL"){
      urlMakers[key.slice(0, -4).toLowerCase()] = makePrefixUrlMaker(cfg[key]);
    }
  }
  return urlMakers;
}(config);


export function createDevToolsWindow (store) {
  if (!__REDUX_DEV_TOOLS__) return;

  const { DevTools, DebugPanel, LogMonitor } = require('redux-devtools/lib/react');
  const win = window.open(
    null,
    'redux-devtools', // give it a name so it reuses the same window
    'menubar=no,location=no,resizable=yes,scrollbars=no,status=no'
  );

  // reload in case it's reusing the same window with the old content
  win.location.reload();

  // wait a little bit for it to reload, then render
  setTimeout(() => {
    React.render(
      <DebugPanel top right bottom left >
        <DevTools store={store} monitor={LogMonitor} />
      </DebugPanel>
      , win.document.body);
  }, 10);
}
