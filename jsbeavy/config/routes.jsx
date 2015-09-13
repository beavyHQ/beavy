import React from "react";
import { Route, DefaultRoute, NotFoundRoute } from "react-router";

/* eslint-disable no-multi-spaces */
// Only import from `route-handlers/*`
import SomePage     from "route-handlers/SomePage";
import ReadmePage   from "route-handlers/ReadmePage";
import HomePage     from "route-handlers/HomePage";
import NotFoundPage from "route-handlers/NotFoundPage";
/* eslint-enable */

// export routes
export default function make_routes(Application){
  // FIXME: make this dynamic
	return (<Route name="app" path="/" handler={Application}>
        		<Route name="some-page" path="/some-page" handler={SomePage} />
        		<Route name="readme" path="/readme" handler={ReadmePage} />
        		<Route name="home" path="/home" handler={HomePage} />
        		<DefaultRoute handler={HomePage} />
        		<NotFoundRoute handler={NotFoundPage} />
        	</Route>
  );
}
