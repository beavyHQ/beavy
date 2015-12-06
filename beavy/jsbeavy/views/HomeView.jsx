import React from 'react'

export class HomeView extends React.Component {
  render () {
    return (
      <div className='container text-center'>
        <img src='http://beavy.xyz/logos/logo.svg' alt='beavy logo' width='150' />
        <h1>Wecome to Beavy!</h1>
        <p>
        Please take a look at the <a href='https://beavyhq.gitbooks.io/beavy-documentation/content/' target='_blank'>documentation</a>.
        </p>
      </div>
    )
  }
}

export default HomeView
