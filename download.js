import 'dotenv/config';
import * as ftp from 'basic-ftp';
import fs from 'fs';
import path from 'path';

const client = new ftp.Client();
client.ftp.verbose = true;

async function ensureLocalDir(dirPath) {
    if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
    }
}

async function downloadDirectory(remotePath, localPath) {
    console.log(`Entering ${remotePath}...`);
    await ensureLocalDir(localPath);

    const list = await client.list(remotePath);

    for (const file of list) {
        const currentRemotePath = path.posix.join(remotePath, file.name);
        const currentLocalPath = path.join(localPath, file.name);

        if (file.isDirectory) {
            // Ignore . and .. and __MACOSX
            if (file.name === '.' || file.name === '..' || file.name === '__MACOSX') continue;

            await downloadDirectory(currentRemotePath, currentLocalPath);
        } else {
            console.log(`Downloading ${file.name} to ${currentLocalPath}...`);
            await client.downloadTo(currentLocalPath, currentRemotePath);
        }
    }
}

async function main() {
    try {
        await client.access({
            host: process.env.FTP_HOST,
            user: process.env.FTP_USER,
            password: process.env.FTP_PASSWORD,
            secure: false
        });

        console.log('Connected. Starting recursive download...');
        await downloadDirectory('/', process.cwd());
        console.log('Download complete.');

    } catch (err) {
        console.error('Error:', err);
    }
    client.close();
}

main();
