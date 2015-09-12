import React from "react";
import { RouteHandler } from "react-router";
import { MainMenu } from "components/MainMenu";
import { createContainer } from "items-store";


import styles from "./twitter.css";

class Application extends React.Component {
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
            <MainMenu />
            <h1>Twitter</h1>
            <RouteHandler />
        </div>;
    }
}

Application.contextTypes = {
    stores: React.PropTypes.object
};


export default createContainer(Application);