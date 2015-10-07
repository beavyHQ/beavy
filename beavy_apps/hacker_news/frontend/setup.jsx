import React from "react";
import { addExtension, getExtensions } from 'config/extensions';
import { Route } from 'react-router';
import { make_url } from 'utils';

import SubmitView from './views/SubmitView';

export function setupViews(Application){
  addExtension('routes',
      <Route name="submit" path="/submit/" component={SubmitView} />);
}