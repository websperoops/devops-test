import React, { Component } from 'react'


class MailchimpCampaign extends Component {
    constructor(props) {
        super(props);

        this.state = {
            hasTitle: false,
            campaignText: ''
        }
        this.numberFormat = new Intl.NumberFormat('us-en', { style: 'currency', currency: 'usd' })

    }

    componentDidMount() {
        const { item } = this.props;
        let campaingText = item.campaign_ref.title || item.campaign_ref.subject_line || item.campaign_ref.preview_text
        this.setState({
            campaignText: campaingText.length > 20 ? `${campaingText.substring(0, 19)}...` : campaingText,
            hasTitle: (item.campaign_ref.title.length > 0)
        })
    }

    render() {
        const { item } = this.props;
        const { hasTitle, campaignText } = this.state;
        return (
            <div className="timeline-container-item d-flex flex-column">
                <img className="timeline-item-icon" src={item.icon} alt="icon" />

                {
                    hasTitle ? (<p className="timeline-item-text"> <b>{item.unique_opens}</b> {item.unique_opens > 1 ? 'people have' : 'person has'} opened your <a target="_blank" style={{ color: '#ef7c15' }} className="font-weight-bold" href={item.campaign_ref.archive_url}>{campaignText}</a> campaign - a <b>{Math.floor(parseFloat(item.open_rate).toFixed(2) * 100)}%  </b>  open rate {Number(item.total_revenue) > 0 ? `generating ${this.numberFormat.format(Number(item.total_revenue))} in sales` : null}!
                    </p>) : <p className="timeline-item-text"><b>{item.unique_opens}</b> {item.unique_opens > 1 ? 'people have' : 'person has'} opened your campaign: <a target="_blank" style={{ color: '#ef7c15' }} className="font-weight-bold" href={item.campaign_ref.archive_url}>{campaignText}</a>  - a  <b>{Math.floor(parseFloat(item.open_rate).toFixed(2) * 100)}%
                    </b> open rate{Number(item.total_revenue) > 0 ? ` generating ${this.numberFormat.format(Number(item.total_revenue))} in sales` : null}!</p>
                }

                <p className="timeline-item-date">{item.date}</p>
                <div className="timeline-connector"></div>
            </div >
        )
    }
}


// const MailchimpCampaign = ({ item }) => {
//     const [campaignText, setCampaignText] = useState('')
//     const [hasTitle, setHasTitle] = useState(false)

//     useEffect(() => {
//         if (item.campaign_ref) {
//             if (item.campaign_ref.title.length > 0) {
//                 setCampaignText(item.campaign_ref.title)
//                 setHasTitle(true)
//             }
//             else if (item.campaign_ref.subject_line) {
//                 if (item.campaign_ref.subject_line.length > 20) {
//                     setCampaignText(item.campaign_ref.subject_line.substring(0, 19) + '...') //get first 20 characters only
//                 }
//                 else {
//                     setCampaignText(item.campaign_ref.subject_line)
//                 }
//             }

//             else {
//                 item.campaign_ref.preview_text && item.campaign_ref.preview_text.length > 20 ? setCampaignText(item.campaign_ref.preview_text.substring(0, 19) + '...') : setCampaignText(item.campaign_ref.preview_text)
//             }
//         }
//     }, [])
// return (
//     <div className="timeline-container-item d-flex flex-column">
//         <img className="timeline-item-icon" src={item.icon} alt="icon" />

//         {
//             hasTitle ? (<p className="timeline-item-text"> <b>{item.unique_opens}</b> {item.unique_opens > 1 ? 'people have' : 'person has'} opened your <a target="_blank" style={{ color: '#ef7c15' }} className="font-weight-bold" href={item.campaign_ref.archive_url}>{campaignText}</a> campaign - a <b>{Math.floor(parseFloat(item.open_rate).toFixed(2) * 100)}%</b> open rate!
//             </p>) : <p className="timeline-item-text"><b>{item.unique_opens}</b> {item.unique_opens > 1 ? 'people have' : 'person has'} opened your campaign: <a target="_blank" style={{ color: '#ef7c15' }} className="font-weight-bold" href={item.campaign_ref.archive_url}>{campaignText}</a>  - a  <b>{Math.floor(parseFloat(item.open_rate).toFixed(2) * 100)}%</b> open rate!</p>
//         }

//         <p className="timeline-item-date">{item.date}</p>
//         <div className="timeline-connector"></div>
//     </div >
// )
// }

export default MailchimpCampaign;