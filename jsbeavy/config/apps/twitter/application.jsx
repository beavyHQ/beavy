import React from "react";
import { MainMenu } from "components/MainMenu";
import { connect } from 'react-redux';

import UserModal from "containers/UserModal";
import UserMenuWidget from "containers/UserMenuWidget";

import { insertExtension } from "config/extensions";

import styles from "./styles/twitterApp.scss";


// make sure User Menu is the first in the list
insertExtension("MainNavigationTools", 0, () => <UserMenuWidget />)

export default class Application extends React.Component {
    static getProps(stores, params) {
        var transition = stores.Router.getItem("transition");
        return {
            loading: !!transition
        };
    }
    render() {
        var { loading } = this.props;
        return <div className={styles.this + (loading ? " " + styles.loading : "")}>
            <div className={styles.loadingElement}>loading...</div>
            <UserModal />
            <MainMenu logo='http://svgporn.com/logos/twitter.svg'/>
            <h1>Twitter</h1>
            {this.props.children}
        </div>;
    }
};
