import * as firebase from "firebase"
import React from "react"
import ReactDOM from "react-dom"

import 'firebase/auth'
import 'firebase/database'

import { Tag } from "@blueprintjs/core"
import "@blueprintjs/icons/lib/css/blueprint-icons.css"
import "@blueprintjs/core/lib/css/blueprint.css"
import "animate.css"

import cat = require("./nyan.gif")

var firebaseConfig = {
    apiKey: "AIzaSyDXyczRuaZWskx43U-Pamzyw1YaUag79lY",
    authDomain: "github-issue-bot.firebaseapp.com",
    databaseURL: "https://github-issue-bot.firebaseio.com",
    projectId: "github-issue-bot",
    storageBucket: "github-issue-bot.appspot.com",
    messagingSenderId: "699789446244",
    appId: "1:699789446244:web:7b2fc9b70a7c64c4986371"
};

firebase.initializeApp(firebaseConfig);

type Issue = {
    date: string
    title: string
    label: string
    project: string
    number: number
}

type State = {
    issues: Issue[]
}

class App extends React.Component<{}, State> {

    constructor(props) {
        super(props)

        this.state = {
            issues: []
        }

        var [db, collection] = this.init()
        this.loadInitialData(collection)

        collection.orderBy("date").onSnapshot((snapshot) => {
            console.log("on snapshot ...");
            this.updateState(snapshot)
        })
    }

    updateState = (snapshot: firebase.firestore.QuerySnapshot) => {
        var issues = []
        snapshot.forEach(x => {
            var data = x.data()
            issues.push({
                label: data["label"],
                title: data["title"],
                project: data["project"],
                date: data["date"],
                number: data["number"]
            })
        });
        this.setState({
            issues: issues.reverse()
        })
    }

    loadInitialData = (collection: firebase.firestore.CollectionReference) => {
        collection.orderBy("date").get().then((snapshot) => {
            this.updateState(snapshot)
        })
    }

    init = (): [firebase.firestore.Firestore, firebase.firestore.CollectionReference] => {
        var db = firebase.firestore()
        var collection = db.collection("issues")
        return [db, collection]
    }

    createLink = (issue: Issue) => {
        var link = `https://github.com/bcircle/${issue.project}/issues/${issue.number}`;
        return link
    }

    render = () =>
        <div>
            <h1>
                <img src={cat} style={{ width: "100px" }} />
            </h1>
            <div>
                {
                    this.state.issues.map(x =>
                        <div style={{ padding: "5px" }} className="animated fadeIn">
                            <span style={{ width: "150px", background: "lightgrey", "padding": "3px", borderRadius: "2px" }}>{x.project}</span>
                            <span style={{ padding: "5px" }}>
                                <a href={this.createLink(x)}>{x.title} (#{x.number}) </a>
                            </span>
                            <Tag intent="primary">{x.label}</Tag>
                        </div>
                    )
                }
            </div>
        </div>
}

var el = document.getElementById("root")
ReactDOM.render(<App />, el)