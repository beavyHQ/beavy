import React from "react";
import { Link } from "react-router";
import { connect } from "react-redux";
import { addExtension } from 'config/extensions';
import config from 'config/config';
import { loadUserLikes } from './actions';

class MenuItem extends React.Component {
  static propTypes = {
    dispatch : React.PropTypes.func
  }

  render() {
    console.log("rendering");
    return (<li><a onClick={(e) => this.props.dispatch(loadUserLikes(1))}>home</a>Test</li>)
  }

}

const ConnectedMenuItem = connect()(MenuItem);

addExtension("MainMenuItem", () => <ConnectedMenuItem />);