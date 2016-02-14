import React from 'react'
import { FormattedMessage, FormattedHTMLMessage } from 'react-intl'

export class HomeView extends React.Component {
  render () {
    return (
      <div className='container text-center'>
        <img src='http://beavy.xyz/logos/logo.svg' alt='beavy logo' width='150' />
        <h1>
          <FormattedMessage
            id='hello-world-title'
            description='Hello World Title'
            defaultMessage='Welcome to Beavy!'
          />
        </h1>
        <FormattedHTMLMessage
          tagname='p'
          id='hello-world-docs-link'
          defaultMessage={'Please take a look at the <a href="{link} target="_blank">documentation</a>.'}
          values={{link: 'https://beavyhq.gitbooks.io/beavy-documentation/content/'}}
        />
      </div>
    )
  }
}

export default HomeView
