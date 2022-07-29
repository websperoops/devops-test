import React, { Component } from 'react'
import FilterItems from './FilterItems'
import TimelineItems from './TimelineItems'
import HomepageHeaderDropdown from '../Homepage/HomepageHeaderDropdown'
import { getIntegrationsList, getSocialTimeRange, getInsightsList, getActiveSub } from '../../api/BLApi'

class Timeline extends Component {
    constructor(props) {
        super(props)

        this.insightsList = {}

        this.integrationsList = []
        this.timerangesList = []

        this.state = {
            loading: true,
            filterIntegrations: [],
            filterInsights: [],
            filterItems: [],
            time: 'All',
            activeSub: false
        }

        Promise.all([getSocialTimeRange(), getInsightsList()]).then(res => {
            this.timerangesList = res[0].map(timerange => timerange.name)
            this.timerangesList.push('All')

            Object.keys(res[1].data).forEach(integration => {
                let insightName = ''

                this.integrationsList.push(integration.charAt(0).toUpperCase() + integration.slice(1))

                if(res[1].data[integration].length > 1) {
                    res[1].data[integration].forEach(insight => {
                        let text = insight.split('_')
                        insightName = ''
                        for(let i = 0; i < text.length - 1; i++) {
                            if(i !== text.length - 2) insightName = insightName + text[i][0].toUpperCase() + text[i].slice(1) + ' '
                            else insightName = insightName + text[i][0].toUpperCase() + text[i].slice(1)
                        }
                        this.insightsList[insightName] = insight
                    })
                } else {
                    let text = res[1].data[integration][0].split('_')
                    for(let i = 0; i < text.length - 1; i++) {
                        if(i !== text.length - 2) insightName = insightName + text[i][0].toUpperCase() + text[i].slice(1) + ' '
                        else insightName = insightName + text[i][0].toUpperCase() + text[i].slice(1)
                    }
                    this.insightsList[insightName] = res[1].data[integration][0]
                }
            })

            this.setState({loading: false, filterInsights: Object.keys(this.insightsList)})
        })

        this.filterIntegrations = this.filterIntegrations.bind(this)
        this.filterInsights = this.filterInsights.bind(this)
    }

    componentDidMount() {
        getActiveSub().then((response) => {
            this.setState({activeSub: response.active_sub})
        })
    }

    filterIntegrations(integrations) {
        let list = []
        Object.keys(this.insightsList).forEach(item => {
            integrations.forEach(integration => {
                if(item.includes(integration)) {
                    list.push(this.insightsList[item])
                }
            })
        })

        if(list.length === 0) {
            list = Object.values(this.insightsList)
        }

        this.setState({filterIntegrations: list})

        let subInsights = []
        if(list.length === 0) {
            subInsights = Object.keys(this.insightsList)
        } else {
            for(const insight in this.insightsList) {
                list.forEach(i => {
                    if(i === this.insightsList[insight]) {
                        subInsights.push(insight)
                    }
                })
            }
        }
        
        this.setState({filterInsights: subInsights})
        this.filterItems(list)
    }

    filterInsights(insights) {
        insights = insights.map(insight => this.insightsList[insight])
        this.filterItems(insights)
    }

    filterItems = (insights) => {
        if(insights.length === 0 && this.state.filterIntegrations.length > 0) {
            this.setState({filterItems: this.state.filterIntegrations})
        } else {
            this.setState({filterItems: insights})
        }
    }

    render() {
        return (
            <div id="timeline-container">
                <div className="d-flex flex-row justify-content-between align-items-baseline timeline-header">
                    <h2 className="homepage-header homepage-header-timeline">Business Timeline</h2>
                    {
                        !this.loading && <>
                            <FilterItems type={'integrations'} filterItemsFunc={this.filterIntegrations} options={this.integrationsList} selectedOptions={this.state.filterIntegrations}/>
                            <FilterItems type={'insights'} filterItemsFunc={this.filterInsights} options={this.state.filterInsights} selectedOptions={Object.keys(this.insightsList)}/>
                            <HomepageHeaderDropdown
                                time={this.state.time}
                                selectTime={(t) => this.setState({time: t})}
                                options={this.timerangesList}
                                type={'timeline'}
                            />
                        </>
                    }
                </div>
                <div className="timeline-container d-flex flex-column">
                { !this.state.activeSub ?
                    null
                    :
                    <TimelineItems time={this.state.time} filterItems={this.state.filterItems}/>
                }
                </div>
            </div>
        )
    }
}

export default Timeline
