/*global __CONFIG__NAME */
import React from 'react'
import { Link } from 'react-router'
import defaultStyles from 'components/MainMenu.scss'
import classnames from 'classnames'

export const styles = defaultStyles

export class MainMenu extends React.Component {
  render () {
    const logo = this.props.logo || 'https://raw.githubusercontent.com/thoughtbot/refills/master/source/images/placeholder_logo_1.png'
    const styles = this.props.styles || defaultStyles

    return <div className={styles.navigation} role='banner'>
      <div className={styles.navigationWrapper}>
        <Link to='/' className={styles.logo}>
          <img src={logo} alt='Logo Image' />
          <span className={styles.title}>{this.props.name || __CONFIG__NAME}</span>
        </Link>
        <a href='' className={styles.navigationMenuButton}>MENU</a>
        <nav class={styles.navigationNav} role='navigation'>
          <ul className={classnames(styles.navigationMenu, styles.show)}>
            {this.props.children}
          </ul>
        </nav>
        <div className={styles.navigationTools}>
          {this.props.navigationTools}
        </div>
      </div>
    </div>
  }
}
