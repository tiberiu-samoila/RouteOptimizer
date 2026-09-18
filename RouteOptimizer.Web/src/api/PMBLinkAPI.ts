import { Response } from '../../types';

class PMBLinkAPI {
    static async getPMBLink(): Promise<Response> {
        return {
            status: 302,
            body: 'https://pmb.ro'
        };
    }

    static async getAllLinks(): Promise<Response> {
        return {
            status: 200,
            body: {
                links: [
                    {
                        name: 'pmb',
                        url: 'https://pmb.ro'
                    }
                ]
            }
        };
    }

    static async getLinkByName(name: string): Promise<Response> {
        if (name.toLowerCase() === 'pmb') {
            return {
                status: 200,
                body: {
                    name: 'pmb',
                    url: 'https://pmb.ro'
                }
            };
        } else {
            return {
                status: 404,
                body: 'Link not found'
            };
        }
    }
}

export default PMBLinkAPI;
