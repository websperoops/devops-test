import "@babel/polyfill"; // Dont Remove!
import React, { Fragment, useReducer, createContext } from 'react';
import ReactDOM from 'react-dom';
import HomepageSummaryRow from './components/Homepage/HomepageSummaryRow';
import DashWidgetGrid from './components/Dashboard/DashWidgetGrid';
import Dashboard from './components/DashboardsV2/Dashboard.jsx';
import DashHeaderMenu from './components/Dashboard/DashHeaderMenu';
import IntegrationServices from './components/Integrations/IntegrationServices'
import SocialContainer from './components/Social/SocialContainer'
import Profile from './components/Profile/Profile';
import Timeline from '../src/components/Timeline/Timeline'
import Feedback from './components/Feedback/FeedBack'
import Navigation from "./components/Navigation/Navigation";
import TopSocialPostRow from './components/Homepage/TopSocialPostRow'
import HomepageHeaderDropdown from './components/Homepage/HomepageHeaderDropdown'
import ReauthModal from './components/Homepage/ReauthModal/ReauthModal'
import { getFavoriteDashboard, getSocialAccounts } from './api/BLApi'

// import {
//   BrowserRouter as Router,
//   Switch,
//   Route,
//   Link
// } from "react-router-dom";
//
// ReactDOM.render(
//   <Router>
//     <Switch>
//       <Route path="/dashboards/homepage/">
//         <HomepageSummaryRow />
//       </Route>
//     </Switch>
//   </Router>,
//   document.getElementById("summaryCharts")
// );

export const ReducerContext = createContext();

if (window.location.href.indexOf("/dashboards/homepage/") > -1) {
    getSocialAccounts().then(res => {
        let { results } = res
        let reauthIntegrations = []
        let shopifyStoreNames = []
        
        for(let i=0; i<results.length; i++) {
            let shopifyStoreName = ''

            if(results[i].extra_data.includes('Force_Reauth')) {
                if(results[i].provider !== 'shopify') {
                    reauthIntegrations.push({provider: results[i].provider})
                } else {
                    let idx = results[i].extra_data.indexOf("'name': ")+8
                    shopifyStoreName = results[i].extra_data.slice(idx)
                    idx = shopifyStoreName.search(",")
                    shopifyStoreName = shopifyStoreName.slice(0, idx).replaceAll("'", "")
                    shopifyStoreNames.push(shopifyStoreName)
                }
            }
        }

        if(shopifyStoreNames.length > 0) {
            reauthIntegrations.push({provider: 'shopify', stores: shopifyStoreNames})
        }

        if(reauthIntegrations.length > 0) {
            ReactDOM.render(<ReauthModal reauthIntegrations={reauthIntegrations}/>,
                document.getElementById("reauth")
            );
        } 

        ReactDOM.render(<><Navigation /><HomepageSummaryRow /></>,
            document.getElementById("summaryCharts")
        );
    
        ReactDOM.render(<><Navigation /><TopSocialPostRow /></>,
            document.getElementById("topSocial")
        );
    
        ReactDOM.render(< Timeline />,
            document.getElementById("timeline")
        );
        
    })

} else if (window.location.href.indexOf("/dashboards/integrations") > -1) {

    var integrationsServices = ReactDOM.render(<><Navigation /><IntegrationServices /></>,
        document.getElementById("integrations")
    );
} 
// else if (window.location.href.indexOf("/dashboards/social") > -1) {
//     console.log('social');
//     var social = ReactDOM.render(<><Navigation /><SocialContainer /></>,
//         document.getElementById("social")
//     );
// } 
else if (window.location.href.indexOf("dashboards/v2") > -1) {

    let dashboardId = window.location.pathname.replace("/dashboards/v2/", "").replace("/", "")

    if (dashboardId) {
        ReactDOM.render(
            <><Navigation /><Dashboard dashboardId={dashboardId} /></>,
            document.getElementById("grid")
        );
    } else {
        getFavoriteDashboard().then(favoriteDashboard => {
            ReactDOM.render(
                <><Navigation /><Dashboard dashboardId={favoriteDashboard.id} /></>,
                document.getElementById("grid")
            );
        })
    }



    // var gridWidgets = ReactDOM.render( <
    //     DashHeaderMenu / > ,
    //     document.getElementById("dash-header-menu")
    // );

} else if (window.location.href.indexOf('/dashboards/profile/') > -1) {
    var profile = ReactDOM.render(<><Navigation /><Profile /></>,
        document.getElementById("user-profile")
    );
} else if (window.location.href.indexOf('/documents_portal') > -1) {
    var documents = ReactDOM.render(< Documents />, document.getElementById('documents'))
    console.log('it works')
} else if (window.location.href.indexOf('/feedback_sent') > -1) {
    var feedback = ReactDOM.render(<><Navigation /></>, document.getElementById('feedback_sent'))
} else if (window.location.href.indexOf('/feedback') > -1) {
    var feedback = ReactDOM.render(<><Navigation />< Feedback /></>, document.getElementById('feedback_content'))
}
