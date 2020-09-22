import Document, { Html, Head, Main, NextScript } from 'next/document';

class MyDocument extends Document {
    static async getInitialProps(ctx) {
        const initialProps = await Document.getInitialProps(ctx);
        return { ...initialProps };
    }

    render() {
        return (
            <Html>
                <Head>
                    <link
                        rel="stylesheet"
                        href="https://fonts.googleapis.com/icon?family=Material+Icons"
                    />
                </Head>
                <body>
                    <Main />
                    <NextScript />
                    <script src="https://d3js.org/d3.v5.min.js" />
                    <script src="/js/manager.js" />
                </body>
            </Html>
        );
    }
}

export default MyDocument;
