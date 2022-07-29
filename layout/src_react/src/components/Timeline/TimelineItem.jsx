import React, { Component } from "react";
import ShopifyOrder from "./ShopifyOrder";
import ShopifyAbandonedCart from './ShopifyAbandonedCart'
import MailchimpCampaign from "./MailchimpCampaign";
import EtsyOrder from "./EtsyOrder";
import QuickbooksAccount from "./QuickbooksAccount";
import QuickbooksBill from "./QuickbooksBill";
import TwitterMention from './TwitterMention'
import InstagramPost from './InstagramPost'
import InstagramStory from './InstagramStory'
import FacebookPost from './FacebookPost'

class Timelineitem extends Component {
  constructor(props) {
    super(props);

    this.dynamicItemMapping = {
      'shopifyOrder': ShopifyOrder,
      'shopifyAbandonedCart': ShopifyAbandonedCart,
      'mailchimpCampaign': MailchimpCampaign,
      'etsyOrder': EtsyOrder,
      'quickbooksAccount': QuickbooksAccount,
      'quickbooksBill': QuickbooksBill,
      'twitterMention': TwitterMention,
      'instagramPost': InstagramPost,
      'instagramStory': InstagramStory,
      'facebookPost': FacebookPost,
    }
  }

  render() {
    const DynamicItem = this.dynamicItemMapping[this.props.item.type]
    return (
      <div>
        <DynamicItem item={this.props.item} />
      </div>
    )
  }
}

export default Timelineitem;
