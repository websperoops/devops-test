import React, { useState, useEffect, useRef } from "react";
import { prototype } from "react-modal";
import {
  Button,
  Modal,
  Card,
  Popover,
  OverlayTrigger,
  Overlay,
} from "react-bootstrap";
import toast, { Toaster } from "react-hot-toast";
import './integrationMenu_integrationServiceBlock.css';
import './integrations.css';


function IntegrationServiceBlock(props) {
  const [info, setInfo] = useState([]);
  const [showTooltip, setShowTooltip] = useState(false); //FOR SHOWING TOOLTIP
  const [target, setTarget] = useState(null);
  const ref = useRef(null);
  useEffect(() => {
    infoSetter();
  }, [props.title]);

  function infoSetter() {
    switch (props.title) {
      case "shopify":
        setInfo({
          details:
            "We connect to your Shopify store to retrieve order, sales, customer, and product information.",
        });
        break;
      case "mailchimp":
        setInfo({
          details:
            "We connect to your MailChimp account to retrieve information about your email marketing campaigns and mailing lists.",
        });
        break;
      case "google":
        setInfo({
          details:
            "We connect to your Google Analytics account to retrieve information about your website traffic, visitors and demographic data.",
        });
        break;

      case "twitter":
        setInfo({
          details:
            "We connect to your Twitter account to retrieve information about your mentions and retweets.",
        });
        break;

      case "facebook":
        setInfo({
          details:
            "We connect to your Facebook account to retrieve information about your page’s activity; impressions, reach, clicks, likes, shares, and ad information.",
        });

        break;
      case "instagram":
        setInfo({
          details:
            "We connect to your Instagram Business account to retrieve information about your page’s activity; impressions, reach, and likes.",
        });
        break;

      case "shipstation:":
        setInfo({
          details:
            "We connect to your ShipStation account to retrieve information about your fulfillment operations; shipping status, package information,shipping costs, and volume",
        });
        break;

      case "etsy":
        setInfo({
          details:
            "We connect to your Etsy store to retrieve order, sales, customer, and product information.",
        });
        break;

      case "quickbooks":
        setInfo({
          details:
            "We connect to your QuickBooks account to retrieve information about your business expenses and vendors.",
        });
        break;
      default:
        setInfo({ details: "Not available" });
    }
  }
  const [showModal, setShowModal] = useState(false); //FOR SHOWING MODAL
  const [selectedstore, setSelectedstore] = useState({});
  const setToast = async (item, isSuccess) => {
    if (isSuccess === true) {
      await toast.success(
        `Successfully deleted ${item.other === "" ? item.email : item.other}`
      );
      setTimeout(function () {
        location.reload();
      }, 2000);
    } else {
      await toast.error(
        `Could not delete ${
          item.other === "" ? item.email : item.other
        }, please visit the ${
          props.title
        } dashboard to uninstall Blocklight manually`
      );
      setTimeout(function () {
        location.reload();
      }, 5000);
    }
  };
  const handleClose = () => {
    setShowModal(false);
    setShowTooltip(false);
  };
  const handleShow = () => setShowModal(true);
  const handleClick = (event, item) => {
    if (event.target != target) {
      setShowTooltip(true);
      setTarget(event.target);
      setSelectedstore(item);
    } else {
      setShowTooltip(!showTooltip);
      setTarget(event.target);
      setSelectedstore(item);
    }
  };
  const handleIntRemoval = (title, id) => {
    if (title === "shopify") {
      fetch(`/dashboards/remove/${title}?id=${id}`).then((res) => {
        if (res.status == 200) {
          setToast(selectedstore, true);
        } else {
          setToast(selectedstore, false);
        }
      });
      // setTimeout(function () {
      //     location.reload()
      // }, 2000)
    } else {
      fetch(`/dashboards/remove/${title}`).then((res) => {
        if (res.status == 200) {
          setToast(selectedstore, true);
        } else {
          setToast(selectedstore, false);
        }
      });
      // setTimeout(function () {
      //     location.reload()
      // }, 2000)
    }
  };
  let formattedData = [];
  if (props.data != undefined) {
    var newJson = props.data.replace(/([a-zA-Z0-9]+?):/g, '"$1":');
    newJson = newJson.replace(/'/g, '"');
    formattedData = JSON.parse(newJson);
  } else {
    let localObj = {};
    localObj["email"] = props.email;
    localObj["other"] = props.other;
    localObj["id"] = 0;
    formattedData.push(localObj);
  }

  return (
    <div className="integration_block">
      <div className="integration_header">
        <img src={props.img} className="integration_logo" />
        <p className="integration_name">{props.title}</p>
        {/* <div className="integration_icons">
                    <i className="fa fa-info tooltip-parent">
                        <div className="tooltip-info">
                            <p>Account: {props.email}</p>
                            {props.title == 'shopify' && <p>Store: {props.other}</p>}
                            <p>{info.details}</p>
                        </div>
                    </i>
                    <i onClick={() => props.ToggleDeleteModal(props.title)} className="fa fa-trash"></i>
                </div> */}
      </div>
      <hr style={{ width: "85%", marginTop: "-0.5rem" }} />
      <div style={{ textAlign: "center" }}>
        <p
          style={{
            marginLeft: "10px",
            marginRight: "10px",
            textAlign: "center",
            fontSize: "12px",
            minHeight: "3.313rem",
          }}
        >
          {info.details}
        </p>
        <p
          style={{
            color: "rgb(239, 124, 21)",
            paddingBottom: "0.6rem",
            cursor: "pointer",
          }}
          onClick={handleShow}
        >
          View <b>{props.count != undefined ? props.count : "1"}</b>{" "}
          {props.count > 1 ? "accounts" : "account"}
        </p>
      </div>
      <Modal
        show={showModal}
        onHide={handleClose}
        backdrop="static"
        keyboard={false}
        style={{ padding: "0" }}
        className="checklist_modal"
      >
        <Modal.Header>
          <Modal.Title style={{ color: "black", textTransform: "capitalize" }}>
            {props.title} Accounts
          </Modal.Title>
        </Modal.Header>
        <Modal.Body className="onboarding-cards">
          <div className="row">
            <div className="col-md-12" ref={ref}>
              <div className="accounts_container">
                <ul
                  className="check_list"
                  style={{ overflowY: "hidden", width: "100%", height: "100%" }}
                >
                  {formattedData.map((item, index) => {
                    return (
                      <>
                        <li className="check_list_item" style={{height: "auto", width: "100%"}} >
                          <img
                            style={{
                              top: "12px",
                              width: "7.5%",
                              marginTop: "3px",
                            }}
                            className="integration_modal_logo"
                            src={props.img}
                            alt=""
                          />
                          <div
                            style={{ marginLeft: "3em" }}
                            className="d-flex flex-column"
                          >
                            <p
                              className="checklist_item_name"
                              style={{
                                minWidth: "13.82rem",
                                textTransform: "none",
                              }}
                            >
                              {item.other === "" ? item.email : item.other}
                            </p>
                          </div>
                          <div
                            style={{ textAlign: "right", position: "relative" }}
                          >
                            <i
                              className="fa fa-trash-o"
                              style={{
                                fontFamily: "fontawesome",
                                fontSize: "1.3rem",
                                cursor: "pointer",
                              }}
                              onClick={() => handleClick(event, item)}
                            ></i>
                            <Overlay
                              show={showTooltip}
                              target={target}
                              placement="top-end"
                              container={ref.current}
                              containerPadding={20}
                              style={{ overflow: "visible" }}
                            >
                              <Popover
                                style={{ zIndex: "1151", overflowY: "visible" }}
                              >
                                <Popover.Title as="h3">
                                  Delete{" "}
                                  {selectedstore.other === ""
                                    ? selectedstore.email
                                    : selectedstore.other}{" "}
                                  ?
                                </Popover.Title>
                                <Popover.Content
                                  style={{
                                    justifyContent: "center",
                                    textAlign: "center",
                                  }}
                                >
                                  <Button
                                    className="grey_button"
                                    onClick={() => setShowTooltip(false)}
                                    style={{
                                      fontSize: "12px",
                                      marginRight: "1rem",
                                    }}
                                  >
                                    Close
                                  </Button>
                                  <Button
                                    className="orange_button"
                                    onClick={() =>
                                      handleIntRemoval(
                                        props.title,
                                        selectedstore.id
                                      )
                                    }
                                    style={{ fontSize: "12px" }}
                                  >
                                    Delete
                                  </Button>
                                </Popover.Content>
                              </Popover>
                            </Overlay>
                          </div>
                          {/* </OverlayTrigger>     */}
                        </li>
                        {index < formattedData.length - 1 ? (
                          <>
                            <hr style={{ width: "75%" }} />
                          </>
                        ) : (
                          <></>
                        )}
                      </>
                    );
                  })}
                </ul>
              </div>
            </div>
          </div>
        </Modal.Body>
        <Modal.Footer style={{ justifyContent: "center" }}>
          <Button className="grey_button" onClick={handleClose}>
            Close
          </Button>
        </Modal.Footer>
      </Modal>

      <Toaster position="bottom-center" reverseOrder={false} />
    </div>
  );
}

export default IntegrationServiceBlock;
