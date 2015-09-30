import React from "react";
import { Link } from "react-router";
import ReactLogo from "elements/ReactLogo";
import { NAME } from 'config/config';
import styles from 'components/MainMenu.scss';
import classnames from 'classnames';
import UserMenuWidget from "containers/UserMenuWidget";

import { getExtensions } from "config/extensions";

export { styles }

export class MainMenu extends React.Component {
	render() {
		const logo = this.props.logo || 'https://raw.githubusercontent.com/thoughtbot/refills/master/source/images/placeholder_logo_1.png',
					styles = this.props.styles || styles;
		return <div className={styles.navigation} role="banner">
					  <div className={styles.navigationWrapper}>
					    <Link to="app" className={styles.logo}>
					      <img src={logo} alt="Logo Image" />
					      <span className={styles.title}>{this.props.name || NAME}</span>
					    </Link>
					    <a href="" className={styles.navigationMenuButton} id="js-mobile-menu">MENU</a>
					    <nav role="navigation">
					      <ul id="js-navigation-menu" className={classnames(styles.navigationMenu, styles.show)}>
					      	{getExtensions('MainMenuItem').map(x=>x.call(this))}
					      </ul>
					    </nav>
					    <div className={styles.navigationTools}>
					    	{getExtensions('MainNavigationTools').map(x=>x.call(this))}
					    </div>
					  </div>
				</div>;
	}
}
