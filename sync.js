import 'dotenv/config';
import * as ftp from 'basic-ftp';
import chokidar from 'chokidar';
import path from 'path';
import { fileURLToPath } from 'url';

const client = new ftp.Client();
client.ftp.verbose = true;

async function uploadFile(filePath) {
    try {
        await client.access({
            host: process.env.FTP_HOST,
            user: process.env.FTP_USER,
            password: process.env.FTP_PASSWORD,
            secure: false // Try false first, or true if explicit TLS is needed
        });

        const remotePath = path.relative(process.cwd(), filePath);
        // Ensure remote directory exists (optional, basic-ftp might handle it or we might need to ensureDir)
        // For now, just try to upload to the root or relative path

        console.log(`Uploading ${filePath} to ${remotePath}...`);
        await client.uploadFrom(filePath, remotePath);
        console.log(`Successfully uploaded ${remotePath} `);

    } catch (err) {
        console.error(`Error uploading ${filePath}: `, err);
    }
    // Note: We're not closing the connection immediately to keep it reused or we can close it. 
    // For a simple watcher, opening/closing per file is safer but slower. 
    // Let's close for now to avoid timeouts.
    client.close();
}

const watcher = chokidar.watch('.', {
    ignored: /(^|[\/\\])\..|node_modules/, // ignore dotfiles and node_modules
    persistent: true,
    ignoreInitial: true // Don't upload everything on start
});

watcher
    .on('add', path => {
        console.log(`File ${path} has been added`);
        uploadFile(path);
    })
    .on('change', path => {
        console.log(`File ${path} has been changed`);
        uploadFile(path);
    });

console.log('Watching for file changes...');
