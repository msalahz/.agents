import { mkdir, readFile, writeFile } from 'node:fs/promises'
import path from 'node:path'
import pngToIco from 'png-to-ico'
import sharp from 'sharp'

type Rgb = { r: number; g: number; b: number }

type Config = {
  source: string
  outputDir: string
  glyphColor: string
  glyphCoverage: number
  touchIcon: { glyphColor: string; background: string; glyphCoverage: number }
  manifest: {
    name: string
    short_name: string
    theme_color: string
    background_color: string
    display: string
  }
}

const configPath = path.resolve(process.argv[2] ?? 'favicons.config.json')
const configDir = path.dirname(configPath)

function hexToRgb(hex: string): Rgb {
  const value = hex.replace('#', '')
  const full = value.length === 3 ? value.split('').map((c) => c + c).join('') : value
  const n = Number.parseInt(full, 16)
  return { r: (n >> 16) & 255, g: (n >> 8) & 255, b: n & 255 }
}

function resolveFrom(base: string, target: string) {
  return path.isAbsolute(target) ? target : path.resolve(base, target)
}

async function loadGlyphAlpha(source: string) {
  return sharp(source).ensureAlpha().trim().extractChannel('alpha').png().toBuffer({ resolveWithObject: true })
}

async function renderGlyph(source: string, size: number, color: Rgb, background: Rgb | null, coverage: number) {
  const { data: alpha, info } = await loadGlyphAlpha(source)
  const glyphSize = Math.round(size * coverage)
  const scale = glyphSize / Math.max(info.width, info.height)
  const width = Math.max(1, Math.round(info.width * scale))
  const height = Math.max(1, Math.round(info.height * scale))

  const fittedAlpha = await sharp(alpha).resize(width, height, { fit: 'fill' }).png().toBuffer()

  const glyph = await sharp({ create: { width, height, channels: 3, background: color } })
    .joinChannel(fittedAlpha)
    .png()
    .toBuffer()

  return sharp({
    create: {
      width: size,
      height: size,
      channels: 4,
      background: background ? { ...background, alpha: 1 } : { r: 0, g: 0, b: 0, alpha: 0 },
    },
  })
    .composite([{ input: glyph, gravity: 'centre' }])
    .png()
    .toBuffer()
}

async function main() {
  const config = JSON.parse(await readFile(configPath, 'utf8')) as Config
  const source = resolveFrom(configDir, config.source)
  const outputDir = resolveFrom(configDir, config.outputDir)
  await mkdir(outputDir, { recursive: true })

  const write = async (fileName: string, buffer: Buffer | string) => {
    await writeFile(path.join(outputDir, fileName), buffer)
    console.log(`wrote ${path.relative(process.cwd(), path.join(outputDir, fileName))}`)
  }

  const glyphColor = hexToRgb(config.glyphColor)
  const transparent = new Map<number, Buffer>()
  for (const size of [16, 32, 48, 192, 512]) {
    transparent.set(size, await renderGlyph(source, size, glyphColor, null, config.glyphCoverage))
  }

  await write('favicon-16x16.png', transparent.get(16)!)
  await write('favicon-32x32.png', transparent.get(32)!)
  await write('android-chrome-192x192.png', transparent.get(192)!)
  await write('android-chrome-512x512.png', transparent.get(512)!)
  await write('favicon.ico', await pngToIco([transparent.get(16)!, transparent.get(32)!, transparent.get(48)!]))

  const touch = config.touchIcon
  await write(
    'apple-touch-icon.png',
    await renderGlyph(source, 180, hexToRgb(touch.glyphColor), hexToRgb(touch.background), touch.glyphCoverage),
  )

  const manifest = {
    ...config.manifest,
    icons: [
      { src: '/android-chrome-192x192.png', sizes: '192x192', type: 'image/png' },
      { src: '/android-chrome-512x512.png', sizes: '512x512', type: 'image/png' },
    ],
  }
  await write('site.webmanifest', JSON.stringify(manifest, null, 2) + '\n')

  console.log(`
Head links to add:
<link rel="icon" href="/favicon.ico" sizes="48x48" />
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
<link rel="manifest" href="/site.webmanifest" />`)
}

main().catch((error: unknown) => {
  console.error(error)
  process.exit(1)
})
