import React, { useState, useEffect } from 'react'

const AccountStep = ({ integrations, handleSetIntegration, handleNextbtn }) => {
    const [chosenIntegration, setChosenIntegration] = useState()

    const integrationChange = (int) => {
        setChosenIntegration(int)
        handleSetIntegration(int)
        handleNextbtn(true)

    }
    useEffect(() => {
        handleNextbtn(false)
    }, [])

    const [imgs, setImgs] = useState([
        { integration: 'facebook', img: '/static/images/facebook-icon.png' },
        { integration: 'shopify', img: '/static/images/shopify-icon.png' },
        { integration: 'mailchimp', img: '/static/images/mailchimp-icon.png' },
        { integration: 'shipstation', img: '/static/images/shipstation-icon.png' },
        { integration: 'google', img: '/static/images/google-icon.png' },
        { integration: 'shopify and mailchimp', img: '/static/images/mail-shop.png' },
        { integration: 'shopify and mailchimp and facebook', img: '/static/images/mail-shop-face.png' },
        { integration: 'shopify and mailchimp and instagram', img: '/static/images/mail-shop-insta.png' },
        { integration: 'shopify and shipstation', img: '/static/images/ship-shop.png' },
        { integration: 'instagram', img: '/static/images/instagram-icon.png' },






    ])


    return (
        <>
            <h4 style={{ opacity: '0.8' }}>Select the account(s) you'd like to use:</h4>
            <div className="d-flex flex-row mt-4 flex-wrap account_item_container justify-content-center">
                {integrations && integrations.map(int => {

                    const imgIndex = imgs.findIndex(img => img.integration === int.toLowerCase());
                    if (imgIndex > -1) {
                        var img = imgs[imgIndex].img
                    }


                    return (<div onClick={() => integrationChange(int)} key={int} className={"account_item d-flex flex-column justify-content-center align-items-center " + (chosenIntegration == int ? 'border-yellow' : '')}>
                        <img src={img} />
                        <p className="text-capitalize mt-2">{int}</p>
                    </div>)
                })}
            </div>
        </>
    )

}

export default AccountStep;