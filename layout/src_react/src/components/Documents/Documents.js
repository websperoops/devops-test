function Documents() {

    const [filesjson, setfilejson] = useState()

    const loadDocuments = async () => {
        const response = await fetch('/api/v1/documents/files');
        const json = await response.json();
        console.log(json)

        // const json1 = {
        //     files: [
        //         { file: 'test1.txt', _file_size: 18, original_filename: "test-file-1.txt", name: 'test1', description: null },
        //         { file: 'test2.txt', _file_size: 18, original_filename: "test-file-2.txt", name: 'test2', description: null },
        //         { file: 'test-3.txt', _file_size: 18, original_filename: "test-file-3-2f.txt", name: 'test2', description: 'hello' }
        //     ]
        // }

        setfilejson(json)
    };



    useEffect(() => {
        loadDocuments();
        document.querySelector('.topbar').style.display = 'none'

    }, [])

    return (
        <Fragment>
            <Logo />
            <div className="container">
                <h2 className="text-center mt-3 mb-3" style={{ color: '#ed7c29' }}>Company Documents</h2>
                <div className="d-flex justify-content-center align-items-end flex-row flex-wrap">

                    {filesjson && filesjson.files.map((file, i) => <DocumentItem original_filename={file.original_filename} path={file.file} key={i} name={file.name} description={file.description} />)}

                </div>
            </div>
        </Fragment>
    )
}

const DocumentItem = (props) => {
    return (
        <div className="m-4 text-center d-flex flex-column" style={{ width: '100px' }}>
            <a className="text-lead" style={{ color: '#ed7c29', marginBottom: '-10px' }} href={`/smedia/filer_private/${props.path}`} target="_blank"><p>{props.name || props.original_filename}</p></a>
            <i className="fa fa-file-pdf-o fa-4x mt-1" style={{ color: '#ff0000', borderTop: '1px solid black', paddingTop: '10px' }} aria-hidden="true"></i>
        </div >
    )
}

const Logo = () => (
    <div className="d-flex justify-center w-100" style={{ position: 'absolute', top: '0' }}>
        <img className="mx-auto" width="300" src="/static/images/Blocklight_Logo_Full_Black.png" />
    </div>
)
