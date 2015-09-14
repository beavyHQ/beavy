import React from "react";
import { Route, DefaultRoute, NotFoundRoute } from "react-router";

/* eslint-disable no-multi-spaces */
// Only import from `route-handlers/*`
import { getExtensions } from "config/extensions";
import HomeView    from 'views/HomeView';
/* eslint-enable */

// export routes
export default function make_routes(Application){
  // FIXME: make this dynamic
  return <Route name="app" path="/" component={Application}>
            {getExtensions('routes')}
            <Route component={HomeView} path="*" />
         </Route>;
}
