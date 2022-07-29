import React, { Component } from 'react'
import { getIntegrationsList } from '../../../../api/BLApi'
import _ from 'underscore'

class AccountStep extends Component {

	constructor(props) {
		super(props);
		this.state = {
			integrations: null
		}

		//TODO: Create (reusable) components of this images(so don't build
		//				the images here by name and path)
		// TODO: Implement key-combinations-dict datatype
		this.integrationsAndIcons = [
			[['facebook'], '/static/images/facebook-icon.png'],
			[['shopify'], '/static/images/shopify-icon.png'],
			[['mailchimp'], '/static/images/mailchimp-icon.png'],
			[['shipstation'], '/static/images/shipstation-icon.png'],
			[['etsy'], '/static/images/etsy.png'],
			[['google'], '/static/images/google-icon.png'],
			[['instagram'], '/static/images/instagram-icon.png'],
			[['shopify', 'mailchimp'], '/static/images/mail-shop.png'],
			[['shopify', 'mailchimp', 'facebook'], '/static/images/mail-shop-face.png'],
			[['shopify', 'mailchimp', 'instagram'], '/static/images/mail-shop-insta.png'],
			[['shopify', 'shipstation'], '/static/images/ship-shop.png'],
		]
		this._matchIntegrationsCombinations = this._matchIntegrationsCombinations.bind(this)
		this._getPathForCombination = this._getPathForCombination.bind(this)
		this._getIntegrationsByNames = this._getIntegrationsByNames.bind(this)
	}

	componentDidMount() {

		getIntegrationsList().then(integrations => {
			this.setState({
				integrations: integrations,
			})
		});
	}

	_matchIntegrationsCombinations(integrationsToMatch) {


		return _.filter(
			this.integrationsAndIcons.map(intsPath => intsPath[0]),
			(ints) => {
				return _.intersection(ints, integrationsToMatch).length == ints.length
			}
		)
	}

	_getPathForCombination(integrationsComb) {
		let matchedCombs = _.filter(
			this.integrationsAndIcons.map(intsPath => intsPath[0]),
			(ints) => (
				(ints.length == integrationsComb.length) &&
				(_.intersection(ints, integrationsComb).length == integrationsComb.length)
			)
		)

		if (!matchedCombs) {
			return null;
		}
		if (matchedCombs.length > 1) {
			console.error("Multiple combinations matched for: " + integrationsComb);
		}

		return _.filter(
			this.integrationsAndIcons,
			(intsPath) => (
				(intsPath[0].length == integrationsComb.length) &&
				(_.intersection(intsPath[0], integrationsComb).length == integrationsComb.length)
			)
		)[0][1]

	}

	_getIntegrationsByNames(integrationsCombNames) {
		return _.filter(
			this.state.integrations,
			i => integrationsCombNames.includes(i.name)
		)
	}

	render() {
		return (
			<div>
				<h4 style={{ opacity: '0.8' }}>Select the account(s) you'd like to use:</h4>
				<div className="d-flex flex-row mt-4 flex-wrap account_item_container justify-content-center">
					{
						this.state.integrations &&
						this._matchIntegrationsCombinations(this.state.integrations.map((intObj) => intObj.name)) &&
						this._matchIntegrationsCombinations(this.state.integrations.map((intObj) => intObj.name)).map(integrationsCombNames => (
							<div
								onClick={() => { this.props.selectValueFunc(this._getIntegrationsByNames(integrationsCombNames)) }}
								key={integrationsCombNames.join()}
								className={
										"account_item d-flex flex-column justify-content-center align-items-center"
										+ (
												(this.props.selectedValue && (
													this.props.selectedValue.map(i => i.name).join() == integrationsCombNames.join()))
													? ' border-yellow'
													: ''
											)
								}
							>
								<img src={this._getPathForCombination(integrationsCombNames)} />
								<p className="text-capitalize mt-2">{integrationsCombNames.join(', ')}</p>
							</div>
						)
						)
					}
				</div>
			</div>
		)
	}
}

export default AccountStep;
