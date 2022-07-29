import React, { Component } from 'react'
import Timelineitem from './TimelineItem.jsx';
import { getPaginatedTimelineData, getChartDataTimeRange, getTimelinePageData } from '../../api/BLApi'

class TimelineItems extends Component {
    constructor(props) {
        super(props)
        this.state = {
            allItems: [],
            items: [],
            page: 1,
            fetchLoading: true,
            buttonText: 'See More',
            time: 'All',
            isFiltered: false
        }

        this.addItems = this.addItems.bind(this)
    }

    componentDidMount() {
        this.addItems(1)
    }

    formatDate(date) {
        var d = new Date(date),
            month = '' + (d.getMonth() + 1),
            day = '' + d.getDate(),
            year = d.getFullYear();
    
        if (month.length < 2) 
            month = '0' + month;
        if (day.length < 2) 
            day = '0' + day;
    
        return [year, month, day].join('-');
    }

    addItems(page) {
        this.setState({isFiltered: false})
        getPaginatedTimelineData(page).then(items => {
            items.forEach(item => {
                switch (item.insight) {
                    case 'shopify_order_feed':
                        item.data.social = 'shopify'
                        item.data.date = new Date(item.data.created_at)
                        item.data.icon = '/static/images/shopify-icon.png'
                        item.data.type = 'shopifyOrder'
                        item.data.insight = 'shopify_order_feed'
                        break;
                    case 'shopify_abandoned_carts_feed':
                        item.data.social = 'shopify'
                        item.data.date = new Date(item.data.created_at)
                        item.data.icon = '/static/images/shopify-icon.png'
                        item.data.type = 'shopifyAbandonedCart'
                        item.data.insight = 'shopify_abandoned_carts_feed'
                        break;
                    case 'mailchimp_campaign_reports_feed':
                        item.data.social = 'mailchimp'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/mailchimp-icon.png'
                        item.data.type = 'mailchimpCampaign'
                        item.data.insight = 'mailchimp_campaign_reports_feed'
                        break;
                    case 'quickbooks_account_info_feed':
                        item.data.social = 'quickbooks'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/quickbooks-icon.png'
                        item.data.type = 'quickbooksAccount'
                        item.data.insight = 'quickbooks_account_info_feed'
                        break;
                    case 'quickbooks_bill_feed':
                        item.data.social = 'quickbooks'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/quickbooks-icon.png'
                        item.data.type = 'quickbooksBill'
                        item.data.insight = 'quickbooks_bill_feed'
                        break;
                    case 'etsy_order_feed':
                        item.data.social = 'etsy'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/etsy-icon.png'
                        item.data.type = 'etsyOrder'
                        item.data.insight = 'etsy_order_feed'
                        break;
                    case 'twitter_mentions_feed':
                        item.data.social = 'twitter'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/twitter-icon.png'
                        item.data.type = 'twitterMention'
                        item.data.insight = 'twitter_mentions_feed'
                        break;
                    case 'instagram_insights_summary_feed':
                        item.data.social = 'instagram'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/instagram-logo.svg'
                        item.data.type = 'instagramPost'
                        item.data.insight = 'instagram_insights_summary_feed'
                        break;
                    case 'instagram_stories_summary_feed':
                        item.data.social = 'instagram'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/instagram-logo.svg'
                        item.data.type = 'instagramStory'
                        item.data.insight = 'instagram_stories_summary_feed'
                        break;
                    case 'facebook_page_posts_summary_feed':
                        item.data.social = 'facebook'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/facebook-logo.svg'
                        item.data.type = 'facebookPost'
                        item.data.insight = 'facebook_page_posts_summary_feed'
                        break;
                    default:
                        return null
                }
                this.setState({ items: [...this.state.items, item.data], allItems: [...this.state.allItems, item.data] })
            })
            this.setState({fetchLoading: false})
        }).catch(error => {
            this.setState({buttonText: 'End of Timeline', fetchLoading: false})
        })
    }

    buildFilter = () => {
        const time = this.props.time
        let filter = ""
        const today = new Date()
        let compareDate = today
        switch(time) {
            case 'Past Hour':
                compareDate.setHours(today.getHours() - 1)
                break;
            case 'Past Day':
                compareDate.setDate(today.getDate()-1)
                break;
            case 'Past Week':
                compareDate.setDate(today.getDate()-7)
                break;
            case 'Past Month':
                compareDate.setMonth(today.getMonth()-1)
                break;
            case 'Past 3 Months':
                compareDate.setMonth(today.getMonth()-3)
                break;
            case 'Past 6 Months':
                compareDate.setMonth(today.getMonth()-6)
                break;
            case 'Past Year':
                compareDate.setFullYear(today.getFullYear()-1)
                break;
            case 'All':
                compareDate = null
                break;
            default:
                compareDate = null
        }

        if (compareDate !== null) {
            const compareDateFormat = this.formatDate(compareDate)
            const timeFilter = '(ts__gt="'+compareDateFormat+'")'
            filter = filter + timeFilter
        }

        return filter
    }

    buildInsightFilter = () => {
        let insightFilter = "&insight="
        if(this.props.filterItems.length > 0) {
            this.props.filterItems.forEach(insight => {
                insightFilter = insightFilter + insight + ","  
            })
        }
        return insightFilter
    }

    filterTimeLine = () => {
        const filter = this.buildFilter()
        const insightFilter = this.buildInsightFilter()
        this.setState({isFiltered : true})
        getTimelinePageData("/business_timeline/", '()', '()', '()', '()', '()', filter, insightFilter, this.state.page).then((response) => {
            response.forEach(item => {
                switch (item.insight) {
                    case 'shopify_order_feed':
                        item.data.social = 'shopify'
                        item.data.date = new Date(item.data.created_at)
                        item.data.icon = '/static/images/shopify-icon.png'
                        item.data.type = 'shopifyOrder'
                        item.data.insight = 'shopify_order_feed'
                        break;
                    case 'shopify_abandoned_carts_feed':
                        item.data.social = 'shopify'
                        item.data.date = new Date(item.data.created_at)
                        item.data.icon = '/static/images/shopify-icon.png'
                        item.data.type = 'shopifyAbandonedCart'
                        item.data.insight = 'shopify_abandoned_carts_feed'
                        break;
                    case 'mailchimp_campaign_reports_feed':
                        item.data.social = 'mailchimp'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/mailchimp-icon.png'
                        item.data.type = 'mailchimpCampaign'
                        item.data.insight = 'mailchimp_campaign_reports_feed'
                        break;
                    case 'quickbooks_account_info_feed':
                        item.data.social = 'quickbooks'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/quickbooks-icon.png'
                        item.data.type = 'quickbooksAccount'
                        item.data.insight = 'quickbooks_account_info_feed'
                        break;
                    case 'quickbooks_bill_feed':
                        item.data.social = 'quickbooks'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/quickbooks-icon.png'
                        item.data.type = 'quickbooksBill'
                        item.data.insight = 'quickbooks_bill_feed'
                        break;
                    case 'etsy_order_feed':
                        item.data.social = 'etsy'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/etsy-icon.png'
                        item.data.type = 'etsyOrder'
                        item.data.insight = 'etsy_order_feed'
                        break;
                    case 'twitter_mentions_feed':
                        item.data.social = 'twitter'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/twitter-icon.png'
                        item.data.type = 'twitterMention'
                        item.data.insight = 'twitter_mentions_feed'
                        break;
                    case 'instagram_insights_summary_feed':
                        item.data.social = 'instagram'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/instagram-logo.svg'
                        item.data.type = 'instagramPost'
                        item.data.insight = 'instagram_insights_summary_feed'
                        break;
                    case 'instagram_stories_summary_feed':
                        item.data.social = 'instagram'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/instagram-logo.svg'
                        item.data.type = 'instagramStory'
                        item.data.insight = 'instagram_stories_summary_feed'
                        break;
                    case 'facebook_page_posts_summary_feed':
                        item.data.social = 'facebook'
                        item.data.date = new Date(item.ts)
                        item.data.icon = '/static/images/facebook-logo.svg'
                        item.data.type = 'facebookPost'
                        item.data.insight = 'facebook_page_posts_summary_feed'
                        break;
                    default:
                        return null
                }
           
                this.setState({ items: [...this.state.items, item.data], allItems: [...this.state.allItems, item.data] })
            })
            this.setState({fetchLoading: false})
        }).catch(error => {
            this.setState({buttonText: 'End of Timeline', fetchLoading: false})
        })
    }

    componentDidUpdate(prevProps) {
        if(prevProps != this.props) {
            if(this.props.filterItems.length > 0 || prevProps.time != this.props.time) {
                this.setState({ isFiltered: true })
                this.setState({ time: prevProps.time })
                this.setState({ items: [], allItems: [] })
                this.filterTimeLine()
            }
            else {
                this.setState({ isFiltered: false })
            }
        }
    }

    handleFetchNext = () => {
        this.setState({fetchLoading: true})
        const newPage = this.state.page + 1;
        this.setState({ page: newPage })
        console.log('Filter', this.state.isFiltered)
        if (this.state.isFiltered) {
            this.filterTimeLine()
        } else {
            this.addItems(newPage)
        }
    }

    render() {
        return (
            <>
                {
                    !!this.state.items && this.state.items.map((item, i) => {
                        item = {...item, date:item.date.toLocaleString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true, month: 'short', year: 'numeric', day: '2-digit' })}
                        return (
                            <Timelineitem item={item} key={i}/>
                        )

                    })
                }
                
                <button style={{ zIndex: 3 }} className="btn_orange btn_long mt-3 mx-auto" onClick={this.handleFetchNext}>{ this.state.fetchLoading ? 'Loading...' : this.state.buttonText }</button>
                    
            </>
        )
    }
}

export default TimelineItems
