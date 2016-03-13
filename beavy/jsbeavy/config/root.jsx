/*global __DEBUG_NW__, __REDUX_DEV_TOOLS__, __CONFIG__URLS_HOME */
import React from 'react'
import { Provider } from 'react-redux'
import { Route, Redirect } from 'react-router'
import { IntlProvider } from 'react-intl'

/* eslint-disable no-multi-spaces */
// Only import from `route-handlers/*`
import { getExtensions } from 'config/extensions'
import setupViews from 'views'

import { ReduxRouter } from 'redux-router'

/* eslint-enable */
export default class Root extends React.Component {
  // routerHistory is provided by the client bundle to determine which
  // history to use (memory, hash, browser). routingContext, on the other hand,
  // is provided by the server and provides a full router state.
  static propTypes = {
    store: React.PropTypes.object.isRequired,
    application: React.PropTypes.func.isRequired
  }

  getRoutes () {
    const routes_by_path = {}
    const remapRoutes = (routes, path = '') => {
      for (let i = routes.length - 1; i >= 0; i--) {
        addRoute(routes[i], path)
      };
    }
    const addRoute = (x, parents = '') => {
      parents = parents.charAt(parents.length - 1) ? parents : parents + '/'
      let path = x.props.path.charAt(0) === '/' ? x.props.path : parents + x.props.path
          // react router creates some weird double-slashes, which are
          // incompatible with our way of looking at urls
          // sanitise them!
      path = path.replace(/(\/\/)/, '/')
      routes_by_path[path] = x
      if (x.props.children) {
        remapRoutes(x.props.children, path)
      }
    }
    const routes = getExtensions('routes')

    remapRoutes(routes)
    if (routes_by_path[__CONFIG__URLS_HOME]) {
      const store = routes_by_path[__CONFIG__URLS_HOME]._store
      if (store) {
        // already assigned
        store.originalProps.path = '/'
        store.props.path = '/'
      } else {
        // not yet handeled, let's fake it
        routes_by_path[__CONFIG__URLS_HOME].props.path = '/'
      }
      routes.push(<Redirect from={__CONFIG__URLS_HOME} to='/' />)
    } else {
      // routes.push(<Route component={HomeView} path='*' />);
    }

    return routes
  }

  render () {
    let debugTools = null

    if (__REDUX_DEV_TOOLS__) {
      const { DevTools, LogMonitor, DebugPanel } = require('redux-devtools/lib/react')
      if (__DEBUG_NW__) {
        const win = window.open(
              null,
              'redux-devtools', // give it a name so it reuses the same window
              'menubar=no,location=no,resizable=yes,scrollbars=no,status=no'
            )

            // reload in case it's reusing the same window with the old content
        win.location.reload()

            // wait a little bit for it to reload, then render
        setTimeout(() => {
          React.render(
                <DebugPanel top right bottom left >
                  <DevTools store={this.props.store} monitor={LogMonitor} />
                </DebugPanel>
                , win.document.body)
        }, 10)
        return
      } else {
        debugTools = (
            <DebugPanel top left bottom key='debugPanel'>
              <DevTools store={this.props.store} monitor={LogMonitor} />
            </DebugPanel>
          )
      }
    }

    setupViews(this.props.application)

    return (
      <div>
        {debugTools}
          <IntlProvider locale='en' messages={ window.PRELOAD.MESSAGES }>
            <Provider store={this.props.store}>
              <ReduxRouter>
                <Route component={this.props.application}>
                  {this.getRoutes()}
                </Route>
              </ReduxRouter>
            </Provider>
          </IntlProvider>
        </div>
    )
  }
}
